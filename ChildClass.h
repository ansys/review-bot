#ifndef CHILD_CLASS_CONTEXT_MODEL_H
#define CHILD_CLASS_CONTEXT_MODEL_H

#include <ParentClass.h>

namespace GlobalContextClassNameSpace
{
  
  // only use this context when defined
  class ChildClass: public ParentClass
  {
    public:
      ChildClass();
      virtual ~ChildClass(){};
      
      virtual int getValue() const override;
  };

inline int ChildClass::getValue() const
{
  return 3;
}


} // GlobalContextClassNameSpace



#endif