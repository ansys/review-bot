"""
This example script demonstrates how to use the OpenAI chat API.

GPT-4 model:
https://platform.openai.com/docs/models/gpt-4

Chat completion API:
https://platform.openai.com/docs/guides/chat

"""
import openai

# CSEBU token
openai.api_key = "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"

prompt = """

Create a c++ class using this democode

#ifndef BASE_CLASS_MODEL_H
#define BASE_CLASS_MODEL_H

namespace BaseClassNameSpace
{
  class BaseClass
  {
    public:
      BaseClass(){};
      ~BaseClass(){};
      
      int getValue();
      
    protected:
        int m_A    = 0;
        double m_B = 0.0;
    
    private:
        std::string name = "";
    };
} 

inline int BaseClass::getValue()
{
  return m_A;
}

#endif

"""

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
        {"role": "system", "content": "You are a very kind programmer."},
        {"role": "user", "content": prompt},
        # {"role": "assistant", "content": init_response},
        # {"role": "user", "content": elab}
    ]
)

text = response['choices'][0].message.content
print(text)
