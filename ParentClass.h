#ifndef PARENT_CLASS_CONTEXT_MODEL_H
#define PARENT_CLASS_CONTEXT_MODEL_H

#include <string>

namespace GlobalContextClassNameSpace
{
  class ParentClass
  {
    public:
      ParentClass();
      ~ParentClass();
      
      virtual int getValue() const = 0;
      
    protected:
        int m_A    = 0;
        double m_B = 0.0;
    
    private:
        std::string name = "";
    };
} // GlobalContextClassNameSpace



#endif