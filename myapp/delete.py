def january(request):
    jan_values = []
    bath=[]
    kitc=[]
    bedr=[]
    dini=[]
    livi=[]
    scatter={}

    # Extract values from BathroomAppliance
    bathroom_appliances = BathroomAppliance.objects.all()
    for appliance in bathroom_appliances:
        bath.append(int(appliance.jan))
    scatter[sum(bath)]="bathroom"

    # Extract values from KitchenAppliance
    kitchen_appliances = KitchenAppliance.objects.all()
    for appliance in kitchen_appliances:
        kitc.append(int(appliance.jan))
    scatter[sum(kitc)]="kitchen"

    # Extract values from BedroomAppliance
    bedroom_appliances = BedroomAppliance.objects.all()
    for appliance in bedroom_appliances:
        bedr.append(int(appliance.jan))
    scatter[sum(bedr)]="bedroom"

    # Extract values from DininghallAppliance
    dininghall_appliances = DininghallAppliance.objects.all()
    for appliance in dininghall_appliances:
        dini.append(int(appliance.jan))
    scatter[sum(dini)]="dining"

    # Extract values from LivingroomAppliance
    livingroom_appliances = LivingroomAppliance.objects.all()
    for appliance in livingroom_appliances:
        livi.append(int(appliance.jan))
    scatter[sum(livi)]="living"
    new=[]
    new.extend([sum(bath),sum(kitc),sum(bedr),sum(dini),sum(livi)])
    
    jan_json = json.dumps(new)

    print(new)
    print(scatter)

    context = {
        'jan': jan_json
    }
    
    return render(request,"january.html",context)