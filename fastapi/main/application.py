from database import Database
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
import uvicorn



app = FastAPI()


class Application:
    database = None
    router = None
    host = 'localhost'
    port = 8888

    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.database = Database()
        self.router = APIRouter()
        self.router.add_api_route(
            '/product', self.get_process, methods=['GET'])
        self.router.add_api_route(
            '/product', self.put_process, methods=['PUT'])
        self.router.add_api_route(
            '/product', self.post_process, methods=['POST'])
        app.include_router(self.router)

    def start(self):
        self.database.connect_to_db()
        uvicorn.run("application:app", host=self.host, port=self.port)

    def get_process(self, id=None, value=None, timestamp=None, limit=None,
                    offset=None):
        fields = {}
        if id:
            try:
                fields['id'] = int(id)
            except Exception:
                return self.client_error('Can not parse "id"')
        if timestamp:
            try:
                fields['timestamp'] = int(timestamp)
            except Exception:
                return self.client_error('Can not parse "timestamp"')
        if value:
            fields['value'] = str(value)
        if limit:
            try:
                limit = int(limit)
                if limit < 0:
                    return self.client_error('Limit is negative')
            except Exception:
                return self.client_error('Can not parse field "limit"')
        if offset:
            try:
                offset = int(offset)
                if offset < 0:
                    return self.client_error('Offset is negative')
            except Exception:
                return self.client_error('Can not parse field "offset"')
        result, error, data = self.database.read_data(fields, limit, offset)
        if result:
            return JSONResponse({'data': data})
        else:
            return JSONResponse({'error': error}, status_code=500)

    async def put_process(self, request: Request):
        id = 0
        value = ''
        try:
            json_data = await request.json()
            if 'id' in json_data:
                try:
                    id = int(json_data['id'])
                except Exception:
                    return self.client_error('Can not parse "id" field')
            else:
                return self.client_error('Field "id" is missing')
            if 'value' in json_data:
                value = str(json_data['value'])
            else:
                return self.client_error('Field "value" is missing')
            result, error = self.database.insert_data(id, value)
            if result:
                return JSONResponse({}, status_code=201)
            else:
                return JSONResponse({'error': error}, status_code=500)
        except Exception:
            return self.client_error('Can not parse received json')

    async def post_process(self, request: Request):
        id = 0
        value = ''
        try:
            json_data = await request.json()
            if 'id' in json_data:
                try:
                    id = int(json_data['id'])
                except Exception:
                    return self.client_error('Can not parse "id" field')
            else:
                return self.client_error('Field "id" is missing')
            if 'value' in json_data:
                value = str(json_data['value'])
            else:
                return self.client_error('Field "value" is missing')
            result, error = self.database.change_data(id, value)
            if result:
                return JSONResponse({})
            else:
                return JSONResponse({'error': error}, status_code=500)
        except Exception:
            return self.client_error('Can not parse received json')

    def client_error(self, error_text):
        print(error_text)
        return JSONResponse({'error': error_text}, status_code=400)
