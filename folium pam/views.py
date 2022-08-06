from django.shortcuts import render
import folium

def index(request):
    location = [35.699690615445995, 51.338090733232264]
    path = folium.Map(location=location, zoom_start=15)

    folium.CircleMarker(
            location=location,
            radius=60,
            popup="Laurelhurst Park",
            color="#3186cc",
            fill=True,
            fill_color="#3186cc",
        ).add_to(path)
    
    folium.Marker(
            location=location,
            popup=folium.Popup(max_width=450), 
            icon=folium.Icon(color="red",icon="fa-home", prefix='fa')
        ).add_to(path)
    

    map = path._repr_html_()

    return render(request, 'index.html', {'map':map})
