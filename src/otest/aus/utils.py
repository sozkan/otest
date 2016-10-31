from oic.utils.time_util import in_a_while

__author__ = 'roland'


RT = {"C": "code", "D": "client cred", "T": "token"}
ATTR = ["profile"]


def to_profile(session, representation="list"):
    p = session["profile"].split(".")
    prof = [RT[p[0]]]

    if representation == "list":
        return prof
    elif representation == "dict":
        ret = {}
        for r in range(0, len(prof)):
            ret[ATTR[r]] = prof[r]
        return ret


def get_profile_info(session, test_id=None):
    try:
        _conv = session["conv"]
    except KeyError:
        pass
    else:
        try:
            iss = _conv.entity.provider_info["issuer"]
        except (TypeError, KeyError):
            iss = ""

        profile = to_profile(session, "dict")

        if test_id is None:
            try:
                test_id = session["testid"]
            except KeyError:
                return {}

        return {"Issuer": iss, "Profile": profile, "Test ID": test_id,
                "Test description": session["node"].desc,
                "Timestamp": in_a_while()}

    return {}


def make_client(**kw_args):
    """
    Have to get own copy of keyjar

    :param kw_args:
    :return:
    """
    c_keyjar = kw_args["keyjar"].copy()
    _cli = Client(client_authn_method=CLIENT_AUTHN_METHOD, keyjar=c_keyjar)

    c_info = {'keyjar': c_keyjar}
    for arg, val in list(kw_args.items()):
        if arg in ['keyjar']:
            continue
        setattr(_cli, arg, val)
        c_info[arg] = val

    return _cli, c_info

# def get_check(check_id):
#     package = ocheck
#     prefix = package.__name__ + "."
#     for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
#                                                          prefix):
#         module = __import__(modname, fromlist="dummy")
#         chk = module.factory(check_id)
#         if chk:
#             return chk
#
#     return aa_check.factory(check_id)
