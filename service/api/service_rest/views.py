from .models import ServiceAppointment, Technician, AutomobileVO
from common.json import ModelEncoder
import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Create your views here.


class TechnicianEncoder(ModelEncoder):
  model = Technician
  properties = ["name", "employee_number", "id"]


class AppointmentEncoder(ModelEncoder):
  model = ServiceAppointment
  properties = [
    "id",
    "VIN",
    "customer_name",
    "time",
    "technician",
    "reason",
    "VIP_treatment",
    "finished"
    ]
  encoders = {
    "technician": TechnicianEncoder(),
  }


class AutomobileVOEncoder(ModelEncoder):
  model = AutomobileVO
  properties = ["vin"]


require_http_methods(["GET", "POST"])
def api_list_technicians(request):
  if request.method == "GET":
    technicians = Technician.objects.all()
    return JsonResponse(
      {"technicians": technicians},
      encoder = TechnicianEncoder,
    )
  else:
    content = json.loads(request.body)
    technician = Technician.objects.create(**content)
    return JsonResponse(
      {"technician": technician},
      encoder=TechnicianEncoder,
      safe=False,
    )




require_http_methods(["GET", "POST"])
def api_list_appointments(request):
  if request.method == "GET":
    service_appointments = ServiceAppointment.objects.all().order_by("time")
    return JsonResponse(
      {"service_appointments": service_appointments},
      encoder = AppointmentEncoder,
    )
  else:
    content = json.loads(request.body)

    try:
      AutomobileVO.objects.get(vin=content["VIN"])
      content["VIP_treatment"] = True
    except AutomobileVO.DoesNotExist:
      content["VIP_treatment"] = False

    try:
      technician = Technician.objects.get(id=content["technician"])
      content["technician"] = technician
    except Technician.DoesNotExist:
      return JsonResponse(
        {"message": "Invalid technician id"},
        status = 400,
      )

    service_appointment = ServiceAppointment.objects.create(**content)
    return JsonResponse(
      service_appointment,
      encoder=AppointmentEncoder,
      safe=False,
    )


require_http_methods(["GET", "DELETE", "PUT"])
def api_detail_appointment(request, pk):
  if request.method == "DELETE":
    count, _ = ServiceAppointment.objects.filter(id=pk).delete()
    return JsonResponse({"delete": count > 0})
  elif request.method == "GET":
    service_appointment = ServiceAppointment.objects.get(id=pk)
    return JsonResponse(
      service_appointment,
      encoder=AppointmentEncoder,
      safe=False,
    )
  else: #PUT
    ServiceAppointment.objects.filter(id=pk).update(finished=True)
    appointment = ServiceAppointment.objects.get(id=pk)
    return JsonResponse(
      appointment,
      encoder=AppointmentEncoder,
      safe=False,
    )


require_http_methods(["GET"])
def api_service_history(request, pk):
  if request.method == "GET":
    vin_appointments = ServiceAppointment.objects.filter(VIN=pk).order_by("time")
    return JsonResponse(
      vin_appointments,
      encoder = AppointmentEncoder,
      safe=False,
    )


require_http_methods(["GET"])
def api_automobile_list(request):
  if request.method == "GET":
    automobiles = AutomobileVO.objects.all()
    return JsonResponse(
      automobiles,
      encoder=AutomobileVOEncoder,
      safe=False,
    )
