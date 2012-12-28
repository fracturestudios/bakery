#include <Python/Python.h>

static PyObject *g_module;

PyObject *import_callback(PyObject *module, PyObject *args)
{
    sleep(1);

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *process_callback(PyObject *module, PyObject *args)
{
    sleep(1);

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *export_callback(PyObject *module, PyObject *args)
{
    sleep(1);

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *extensions(PyObject *module, PyObject *args)
{
    PyObject *import_callback = 
        PyObject_GetAttrString(g_module, "import_callback");
    PyObject *process_callback = 
        PyObject_GetAttrString(g_module, "process_callback");
    PyObject *export_callback = 
        PyObject_GetAttrString(g_module, "export_callback");

    PyObject *imp_exts = PyList_New(0);
    PyList_Append(imp_exts, PyString_FromString("test"));

    PyObject *imp = PyDict_New();
    PyDict_SetItemString(imp, "TestImporter", 
                         PyTuple_Pack(2, imp_exts, import_callback));

    PyObject *proc = PyDict_New();
    PyDict_SetItemString(proc, "TestProcessor", process_callback);

    PyObject *exp = PyDict_New();
    PyDict_SetItemString(exp, "TestExporter", export_callback);

    return PyTuple_Pack(3, imp, proc, exp);
}

static PyMethodDef TestMethods[] = 
{
    { "extensions", extensions, METH_VARARGS, "Enumerates extensions" },
    { "import_callback", import_callback, METH_VARARGS, "Import something" },
    { "process_callback", process_callback, METH_VARARGS, "Process something" },
    { "export_callback", export_callback, METH_VARARGS, "Export something" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC inittest(void)
{
    g_module = Py_InitModule("test", TestMethods);
}

