#include <stdlib.h>
#include <stdio.h>
#include <Python.h>


PyObject* curils_mult_matrix(PyObject* self, PyObject* args)
{
    PyObject* arr1 = NULL;
    PyObject* arr2 = NULL;
    if (!PyArg_ParseTuple(args, "OO", &arr1, &arr2))
    {
        printf("ERROR: Failed to parse argument");
        return NULL;
    }
    long R1 = PyList_Size(arr1);
    long C1 = PyList_Size(PyList_GetItem(arr1, 0));
    long C2 = PyList_Size(PyList_GetItem(arr2, 0));
    long R2 = PyList_Size(arr2);
    if (C1 != R2)
    {
        return NULL;
    }
    long res[R1][C2];
    
    for (int i = 0; i < R1; i++)
        for (int j = 0; j < C2; j++)
        {
            res[i][j] = 0;
            for (int k = 0; k < R2; k++)
            {
                PyObject *tmp1 = PyList_GetItem(PyList_GetItem(arr1, i), k);
                PyObject *tmp2 = PyList_GetItem(PyList_GetItem(arr2, k), j);
                res[i][j] += PyLong_AsLong(tmp1) * PyLong_AsLong(tmp2);
            }
        }
    PyObject *rarr = PyList_New(R1);
    for (int i = 0; i < R1; i++)
    {
        PyObject *lst = PyList_New(C2);
        if (!lst)
            return NULL;
        for (int j = 0; j < C2; j++)
        {
            PyList_SET_ITEM(lst, j, Py_BuildValue("l",res[i][j]));
        }
        PyList_SET_ITEM(rarr, i, lst);
    }
    return rarr;
}

static PyMethodDef methods[] = {
    { "mult_matrix", curils_mult_matrix, METH_VARARGS, "multiply two matrix"},
    { NULL, NULL, 0, NULL}
};

static struct PyModuleDef cutils_module = {
    PyModuleDef_HEAD_INIT, "cutils_mult_matrix",
    NULL, -1, methods
};

PyMODINIT_FUNC PyInit_cutils(void){
    return PyModule_Create( &cutils_module );
}

