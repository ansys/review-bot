#include "ParentClass.h"

using namespace GlobalContextClassNameSpace;

ParentClass::ParentClass()
: m_A(0)
, m_B(0.0)
, m_name("hello")
{
    std::cout << "ParentClass:" << m_name << std::endl;
}

ParentClass::~ParentClass() 
{
   
}

