#include <Python/Python.h>

PyObject *test_main(PyObject *self, PyObject *args)
{
    const char *cmd;
    int ret;

    if (!PyArg_ParseTuple(args, "s", &cmd))
        return NULL;

    ret = system(cmd);

    return Py_BuildValue("i", ret);
}

static PyMethodDef TestMethods[] = 
{
    { "main", test_main, METH_VARARGS, "system()" },
    { NULL, NULL, 0, NULL },
};

PyMODINIT_FUNC inittest(void)
{
    PyObject *m;
     
    m = Py_InitModule("test", TestMethods);
}

