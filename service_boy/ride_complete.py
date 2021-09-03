def ride_complete(trip_ID, stop_customer_time, Customer_Service_Hist, Service_Boy_Service_Hist, Customer_Ongoing_Trip, Service_Boy_Ongoing_Trip):
    print('working')

    customer_ongoing_trip = Customer_Ongoing_Trip.objects.filter(
        customer_trip_id=int(trip_ID))

    service_boy_ongoing_trip = Service_Boy_Ongoing_Trip.objects.filter(
        service_boy_trip_id=int(trip_ID))

    customer_service_hist = Customer_Service_Hist.objects.filter(
        customer_trip_id=int(trip_ID))
    customer_service_hist.update(
        time_taken=stop_customer_time,
        status='Ride Completed',
        start_date_time=customer_ongoing_trip[0].start_date_time
    )

    service_boy_service_hist = Service_Boy_Service_Hist.objects.filter(
        service_boy_trip_id=int(trip_ID))
    service_boy_service_hist.update(
        time_taken=stop_customer_time,
        status='Ride Completed',
        start_date_time=service_boy_ongoing_trip[0].start_date_time
    )

    service_boy_ongoing_trip.delete()
    customer_ongoing_trip.delete()

    print(customer_service_hist)
    print(customer_ongoing_trip)
    print(service_boy_service_hist)
    print(service_boy_ongoing_trip)
