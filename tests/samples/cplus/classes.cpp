"""A class sample which includes errors a junior developer might run into"""


#include <iostream>

class Animal 
{
public:
    void eat() {
        std::cout << "The animal is eating." << std::endl;
    }
};

class Dog: public Animal 
{
public:
    Dog() : Animal() {} 
    void bark() {
        std::cout << "The dog is barking." << std::endl;
    }
};

class GermanShepherd: public Dog 
{
public:
    void barkk() { 
        std::cout << "The German Shepherd is barking." << std::endl;
    }
};

int main() {
    GermanShepherd gs;
    gs.eat();
    gs.barkk();
    return 0;
}
