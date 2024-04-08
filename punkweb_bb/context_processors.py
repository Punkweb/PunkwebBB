from punkweb_bb.conf import PUNKWEB_CONF as conf


def punkweb_bb_conf(request):
    return {
        "conf": conf,
    }
