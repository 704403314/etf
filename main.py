from wsgiref.simple_server import make_server
import akshare as ak
import json

connStr = '''
{ 
"code" : 0, 
"msg" : "SUCCESS 成功"
}
'''

errStr = '''
{ 
"code" : -1, 
"msg" : "404 not found"
}
'''


def RunServer(environ, start_response):
    # 添加回复内容的HTTP头部信息，支持多个
    headers = {'Content-Type': 'application/json', 'Custom-head1': 'Custom-info1'}

    # environ 包含当前环境信息与请求信息，为字符串类型的键值对
    current_url = environ['PATH_INFO']
    current_content_type = environ['CONTENT_TYPE']
    # current_content_length = environ['CONTENT_LENGTH']
    current_request_method = environ['REQUEST_METHOD']
    current_remote_address = environ['REMOTE_ADDR']
    # current_encode_type = environ['PYTHONIOENCODING']        #获取当前文字编码格式，默认为UTF-8
    '''
    HTTP客户端请求的其他头部信息（Host、Connection、Accept等），对应environ内容为“HTTP_XXX”，
    例如：请求头部为"custom-header: value1",想获取custom-header的值使用如下方式：
    '''
    # current_custom_header = environ['HTTP_CUSTOM_HEADER']

    # 获取 body JSON内容转换为python对象
    # current_req_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    # current_req_json = json.loads(current_req_body)

    # 打印请求信息
    # print("environ:", environ)
    print("REQUEST remote ip:", current_remote_address)
    print("REQUEST method:", current_request_method)
    print("REQUEST URL:", current_url)
    print("REQUEST Content-Type:", current_content_type)
    # print("REQUEST Custom-header:", current_custom_header)
    # print("REQUEST body:", current_req_json)

    # 根据不同URL回复不同内容
    if current_url == "/connect":
        # df = ak.fund_etf_hist_sina(symbol="sh517090")
        code_info = environ['QUERY_STRING']
        code = code_info.replace("code=", "")
        df = ak.fund_open_fund_info_em(fund=code)
        # df = ak.fund_etf_hist_em(symbol="517090", period="daily", start_date="20200421", end_date="20230421",
        # adjust="")

        # df['交易日期'] = pd.to_datetime(df['date'])
        # df.set_index('交易日期', inplace=True)
        # df = df['2022/04/21': '2023/04/21']

        res = df.to_json(orient="records", force_ascii=False)
        start_response("200 ok", list(headers.items()))
        # print("res:", res)
        # print("code:", code)
        return [res.encode("utf-8"), ]
    if current_url == "/guzhi":
        # print("guzhi:", 123)
        df = ak.index_value_name_funddb()
        # print("df:", df)
        res = df.to_json(orient="records", force_ascii=False)
        start_response("200 ok", list(headers.items()))
        # print("res:", res)
        return [res.encode("utf-8"), ]
    if current_url == "/open":
        df = ak.fund_open_fund_rank_em(symbol="全部")

        res = df.to_json(orient="records", force_ascii=False)
        start_response("200 ok", list(headers.items()))
        # print("res:", res)
        return [res.encode("utf-8"), ]
    if current_url == "/changnei":
        df = ak.fund_exchange_rank_em()

        res = df.to_json(orient="records", force_ascii=False)
        start_response("200 ok", list(headers.items()))
        # print("res:", res)
        return [res.encode("utf-8"), ]
    if current_url == "/huobi":
        df = ak.fund_money_rank_em()

        res = df.to_json(orient="records", force_ascii=False)
        start_response("200 ok", list(headers.items()))
        # print("res:", res)
        return [res.encode("utf-8"), ]
    if current_url == "/licai":
        df = ak.fund_lcx_rank_em()

        res = df.to_json(orient="records", force_ascii=False)
        start_response("200 ok", list(headers.items()))
        # print("res:", res)
        return [res.encode("utf-8"), ]
    if current_url == "/shishi":
        code_info = environ['QUERY_STRING']
        code = code_info.replace("code=", "")
        df = ak.fund_value_estimation_em(symbol="全部")

        res = df.to_json(orient="records", force_ascii=False)
        # s1 = json.loads(res)
        return_obj = json.dumps({})
        parsed_array = json.loads(res)
        for item in parsed_array:
            if item['基金代码'] == code:
                return_obj = json.dumps(item)
                break

        if return_obj == json.dumps({}):
            df = ak.fund_value_estimation_em(symbol="场内交易基金")

            res = df.to_json(orient="records", force_ascii=False)
            parsed_array = json.loads(res)
            for item in parsed_array:
                if item['基金代码'] == code:
                    return_obj = json.dumps(item)
                    break

        start_response("200 ok", list(headers.items()))
        # return [s1["data"].encode("utf-8"), ]
        return [return_obj.encode("utf-8"), ]
    if current_url == "/shishi/many":
        code_info = environ['QUERY_STRING']
        code = code_info.replace("code=", "")
        df = ak.fund_value_estimation_em(symbol="全部")

        res = df.to_json(orient="records", force_ascii=False)
        # s1 = json.loads(res)
        return_obj = json.dumps({})
        parsed_array = json.loads(res)
        code_list = code.split(",")
        print("code_list", code_list)
        code_dict = {}

        for item in parsed_array:
            if item['基金代码'] in code_list:
                code_dict[item['基金代码']] = item
                if len(code_dict) == len(code_list):
                    break

        print(len(code_dict), len(code_list))
        if len(code_dict) != len(code_list):
            internal = ak.fund_value_estimation_em(symbol="场内交易基金")
            internal_res = internal.to_json(orient="records", force_ascii=False)
            parsed_array = json.loads(internal_res)
            for item in parsed_array:
                if item['基金代码'] in code_list:
                    code_dict[item['基金代码']] = item
                    if len(code_dict) == len(code_list):
                        break

        return_list = []
        for value in code_dict.values():
            return_list.append(value)
        print(code_dict)
        print(return_list)

        start_response("200 ok", list(headers.items()))
        return [json.dumps(return_list).encode("utf-8"), ]
    else:
        print("current_url", current_url)
        start_response("404 not found", list(headers.items()))
        return [errStr.encode("utf-8"), ]


if __name__ == "__main__":
    # 8081为HTTP服务监听端口，自行修改
    httpd = make_server('', 8089, RunServer)
    host, port = httpd.socket.getsockname()
    print('Serving running', host, 'port', port)
    httpd.serve_forever()
