#ifndef CHILD_CLASS_CONTEXT_MODEL_H
#define CHILD_CLASS_CONTEXT_MODEL_H

#include <ParentClass.h>

namespace GlobalContextClassNameSpace
{
  
  class ChildClass: public ParentClass
  {
      ChildClass(){};
      ~ChildClass(){};
      
      virtual int getValue() const override;
  };

inline int ChildClass::getValue() const
{
  return 3;
}


} // GlobalContextClassNameSpace



#endif