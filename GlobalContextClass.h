#ifndef GLOBAL_CONTEXT_CLASS_MODEL_H
#define GLOBAL_CONTEXT_CLASS_MODEL_H

#include <string>

namespace GlobalContextNameSpace
{
  class ParentClass
  {
    public:
      ParentClass();
      ~ParentClass();
      
      virtual int getValue();
      
    protected:
        int m_A    = 0;
        double m_B = 0.0;
    
    private:
        std::string name = "";
    };

   class  
} // GlobalContextNameSpace

inline int ParentClass::getValue()
{
  return m_A;
}



#endif