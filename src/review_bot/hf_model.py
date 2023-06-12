"""Module for HuggingFace model implementations."""
import logging

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    StoppingCriteria,
    StoppingCriteriaList,
)

LOG = logging.getLogger(__name__)


class StopOnTokens(StoppingCriteria):
    """Wrapper for stop token strings.

    Determines on which tokens the model should stop the inference.

    Parameters
    ----------
    tokenizer : AutoTokenizer
        Tokenizer that will be used with the model.
    stopwords : list, optional
        Words that will mark the end of the inference.
    """

    def __init__(self, tokenizer, stopwords=["<|im_end|>", "<|endoftext|>"]):
        """Initialize the stop tokens."""
        self.stop_token_ids = tokenizer.convert_tokens_to_ids(stopwords)

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        """Run when called from the model inference.

        Parameters
        ----------
        input_ids : torch.LongTensor
            IDs of the input tokens.
        scores : torch.FloatTensor
            Score of the tokens.

        Returns
        -------
        bool
            Whether to stop the inference or not.
        """
        for stop_id in self.stop_token_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


class Inference:
    """Wrapper for HuggingFace text generation models.

    Parameters
    ----------
    model_name : str, optional
        Name of the model in HuggingFace, by default "chavinlo/alpaca-13b"
    tokenizer_name : str, optional
        Name of the tokenizer in HuggingFace, by default "chavinlo/gpt4-x-alpaca"
    """

    def __init__(
        self, model_name="mosaicml/mpt-7b", tokenizer_name: str = "mosaicml/mpt-7b"
    ):
        """Initialize the model and the tokenizer."""
        self.device = "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, trust_remote_code=True, load_in_8bit=True, device_map="auto"
        )
        print(self.model.get_memory_footprint())

    def evaluate(
        self,
        instruction: str,
        input: str = None,
        temperature: float = 0.1,
        top_p: float = 0.75,
        top_k=40,
        num_beams=4,
        max_new_tokens=128,
        **kwargs,
    ):
        """Perform the inference of the model.

        Parameters
        ----------
        instruction : str
            Query we want to ask the model.
        input : str, optional
            Additional context we can add to the query, by default None.
        temperature : float, optional
            _description_, by default 0.1
        top_p : float, optional
            _description_, by default 0.75
        top_k : int, optional
            _description_, by default 40
        num_beams : int, optional
            _description_, by default 4
        max_new_tokens : int, optional
            _description_, by default 128

        Returns
        -------
        str
            Result from the query.
        """
        stop = StopOnTokens(self.tokenizer)

        prompt = self._generate_prompt(instruction, input)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            **kwargs,
        )
        with torch.no_grad():
            generation_output = self.model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
                stopping_criteria=StoppingCriteriaList([stop]),
            )
        s = generation_output.sequences[0]
        output_str = self.tokenizer.decode(s)

        try:
            output_str = output_str.split("### Response:")[1]
        except IndexError:
            LOG.warning("Output might be malformed.")
        output_str = output_str.replace("<|endoftext|>", "")
        output_str = output_str.replace("<|im_end|>", "")

        return output_str
