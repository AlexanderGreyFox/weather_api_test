from aiohttp import web
import json


def json_err(status_code: int, exception: Exception) -> web.Response:
    """
    Create json with error status and info from exception
    :param status_code:
    :param exception:
    :return:
    """

    return web.Response(status=status_code,
                        body=json.dumps({
                                            'error': exception.__class__.__name__,
                                            'detail': str(exception)
                                        }).encode('utf-8'),
                        content_type='application/json')


@web.middleware
def exception_catcher(request: web.Request, handler) -> web.Response:
    """
    Catcher for all exception situations
    :param request:
    :param handler:
    :return:
    """

    try:
        resp = await handler(request)
        status = resp.status
        if status != 200 or status != 202 or status != 204:
            return json_err(status, Exception(resp.message))
        return resp
    except Exception as ex:
        return json_err(500, ex)
