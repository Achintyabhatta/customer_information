from rest_framework.views import Response
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError)
import json

# Helper function to send success response back to the Client | Error Handled
def WriteSuccessMessage(message):
    return Response({ 'status' : 'Success', 'status_code' : 200, 'message' : message, "data" : ""})   

# Helper function to send success response along with response data back to the Client | Error Handled
def WriteSuccessMessageWithData(data):
    return Response({'status' : 'Success', 'status_code' : 200, 'data' : data, "message" : "" })

# Helper function to send Bad request response to the client in the event of Invalid Params passed | Error Handled
def WriteErrorMessageBadRequest(message):
    response = json.dumps({"status" : "Error", "message" : message, "data" : ""})
    return HttpResponseBadRequest(response, content_type='application/json')

# Helper function to send Server Error response  to the client in the event of some faliure at the server end | Error Handled
def WriteErrorMessageInternalServerError(message):
    response = json.dumps({"status" : "Error", "message" : message, "data" : ""})
    return HttpResponseServerError(response, content_type='application/json')