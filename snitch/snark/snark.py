from ctypes import *
import os

_lib = None


class Prover:
    def __init__(self, pk_file_location):
        global _lib
        if _lib is None:
            _lib = cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_snark.so'))

        self._InitProvingModule = _lib.InitProvingModule
        self._InitProvingModule.argtypes = [POINTER(c_char)]
        self._InitProvingModule.restype = None

        self._GetKey = _lib.GetKey
        self._GetKey.argtypes = [POINTER(c_char), POINTER(c_char), POINTER(POINTER(c_char)), POINTER(c_int),
                                 POINTER(POINTER(c_char)), POINTER(c_int)]
        self._GetKey.restype = None

        self._CreateSNARK = _lib.CreateSNARK
        self._CreateSNARK.argtypes = [POINTER(c_char), c_int, POINTER(c_char), c_int, POINTER(c_char), POINTER(c_char),
                                      POINTER(POINTER(c_char)), POINTER(c_int), POINTER(POINTER(c_char)),
                                      POINTER(c_int), POINTER(POINTER(c_char)), POINTER(c_int),
                                      POINTER(POINTER(c_char)), POINTER(c_int)]
        self._CreateSNARK.restype = None

        c_pk_file_location = c_char_p(str.encode(pk_file_location))
        self._InitProvingModule(c_pk_file_location)

    def get_key(self, username, password):
        c_user = c_char_p(str.encode(username))
        c_pass = c_char_p(str.encode(password))
        c_secret_key = POINTER(c_char)()
        c_secret_key_len = c_int()
        c_public_key = POINTER(c_char)()
        c_public_key_len = c_int()
        self._GetKey(c_user, c_pass, c_secret_key, c_secret_key_len, c_public_key, c_public_key_len)
        secret_key = b''.join(c_secret_key[i] for i in range(c_secret_key_len.value))
        public_key = b''.join(c_public_key[i] for i in range(c_public_key_len.value))
        return secret_key, public_key

    def create_snark(self, secret_key, tree_path, topic, comment):
        c_secret_key = c_char_p(secret_key)
        c_secret_key_len = c_int(len(secret_key))
        c_tree_path = c_char_p(tree_path)
        c_tree_path_len = c_int(len(tree_path))
        c_topic = c_char_p(str.encode(topic))
        c_comment = c_char_p(str.encode(comment))
        c_snark = POINTER(c_char)()
        c_snark_len = c_int()
        c_comment_id = POINTER(c_char)()
        c_comment_id_len = c_int()
        c_comment_sig = POINTER(c_char)()
        c_comment_sig_len = c_int()
        c_root = POINTER(c_char)()
        c_root_len = c_int()
        self._CreateSNARK(c_secret_key, c_secret_key_len, c_tree_path, c_tree_path_len, c_topic, c_comment,
                          byref(c_snark), byref(c_snark_len), byref(c_comment_id), byref(c_comment_id_len),
                          byref(c_comment_sig), byref(c_comment_sig_len), byref(c_root), byref(c_root_len))
        snark = b''.join(c_snark[i] for i in range(c_snark_len.value))
        comment_id = b''.join(c_comment_id[i] for i in range(c_comment_id_len.value))
        comment_sig = b''.join(c_comment_sig[i] for i in range(c_comment_sig_len.value))
        root = b''.join(c_root[i] for i in range(c_root_len.value))
        return snark, comment_id, comment_sig, root


class Verifier:
    def __init__(self, vk_file_location):
        global _lib
        if _lib is None:
            _lib = cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_snark.so'))

        self._InitVerifyingModule = _lib.InitVerifyingModule
        self._InitVerifyingModule.argtypes = [POINTER(c_char)]
        self._InitVerifyingModule.restype = None

        self._VerifySNARK = _lib.VerifySNARK
        self._VerifySNARK.argtypes = [POINTER(c_char), c_int, POINTER(c_char), c_int, POINTER(c_char),
                                      POINTER(c_char), POINTER(c_char), c_int, POINTER(c_char), c_int,
                                      POINTER(c_bool), POINTER(POINTER(c_char)), POINTER(c_int)]
        self._VerifySNARK.restype = None

        c_vk_file_location = c_char_p(str.encode(vk_file_location))
        self._InitVerifyingModule(c_vk_file_location)

    def verify_snark(self, snark, root, topic, comment, comment_id, comment_sig):
        c_snark = c_char_p(snark)
        c_snark_len = c_int(len(snark))
        c_root = c_char_p(root)
        c_root_len = c_int(len(root))
        c_topic = c_char_p(str.encode(topic))
        c_comment = c_char_p(str.encode(comment))
        c_comment_id = c_char_p(comment_id)
        c_comment_id_len = c_int(len(comment_id))
        c_comment_sig = c_char_p(comment_sig)
        c_comment_sig_len = c_int(len(comment_sig))
        c_result = c_bool()
        c_result_description = POINTER(c_char)()
        c_result_description_len = c_int()
        self._VerifySNARK(c_snark, c_snark_len, c_root, c_root_len, c_topic, c_comment, c_comment_id, c_comment_id_len,
                          c_comment_sig, c_comment_sig_len, byref(c_result), byref(c_result_description),
                          byref(c_result_description_len))
        result = c_result.value
        result_descr = (b''.join(c_result_description[i] for i in range(c_result_description_len.value))).decode(
            'utf-8')
        return result, result_descr


class MerkleTree:
    def __init__(self, tree_file_location, index_file_location):
        global _lib
        if _lib is None:
            _lib = cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_snark.so'))

        self._InitTreeModule = _lib.InitTreeModule
        self._InitTreeModule.argtypes = [POINTER(c_char), POINTER(c_char)]
        self._InitTreeModule.restype = None

        self._AddToTree = _lib.AddToTree
        self._AddToTree.argtypes = [POINTER(c_char), c_int]
        self._AddToTree.restype = None

        self._CheckInTree = _lib.CheckInTree
        self._CheckInTree.argtypes = [POINTER(c_char), c_int, POINTER(c_bool)]
        self._CheckInTree.restype = None

        self._GetTreeRoot = _lib.GetTreeRoot
        self._GetTreeRoot.argtypes = [POINTER(POINTER(c_char)), POINTER(c_int)]
        self._GetTreeRoot.restype = None

        self._GetTreePath = _lib.GetTreePath
        self._GetTreePath.argtypes = [POINTER(c_char), c_int, POINTER(POINTER(c_char)), POINTER(c_int)]
        self._GetTreePath.restype = None

        c_tree_file_location = c_char_p(str.encode(tree_file_location))
        c_index_file_location = c_char_p(str.encode(index_file_location))
        self._InitTreeModule(c_tree_file_location, c_index_file_location)

    def add(self, value):
        c_value = c_char_p(value)
        c_value_len = c_int(len(value))
        self._AddToTree(c_value, c_value_len)

    def check(self, value):
        c_value = c_char_p(value)
        c_value_len = c_int(len(value))
        c_result = c_bool()
        self._CheckInTree(c_value, c_value_len, byref(c_result))
        result = c_result.value
        return result

    def get_root(self):
        c_root = POINTER(c_char)()
        c_root_len = c_int()
        self._GetTreeRoot(byref(c_root), byref(c_root_len))
        root = b''.join(c_root[i] for i in range(c_root_len.value))
        return root

    def get_path(self, value):
        c_value = c_char_p(value)
        c_value_len = c_int(len(value))
        c_path = POINTER(c_char)()
        c_path_len = c_int()
        self._GetTreePath(c_value, c_value_len, byref(c_path), byref(c_path_len))
        path = b''.join(c_path[i] for i in range(c_path_len.value))
        return path
