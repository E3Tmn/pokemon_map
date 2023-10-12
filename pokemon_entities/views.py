import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
import datetime
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time = datetime.datetime.now(tz=timezone.utc)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon,
                                                       appeared_at__lt=time,
                                                       disappeared_at__gt=time
                                                       )
        for pokemon_entity in pokemon_entities:
            print(pokemon_entity.lat)
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time = datetime.datetime.now(tz=timezone.utc)
    pokemon_on_page = {}
    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemons = PokemonEntity.objects.filter(pokemon=pokemon,
                                                       appeared_at__lt=time,
                                                       disappeared_at__gt=time
                                                       )
            for pokemon_entity in requested_pokemons:
                add_pokemon(
                    folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(pokemon_entity.pokemon.photo.url),
                )
            pokemon_on_page.setdefault('pokemon_id', pokemon.id)
            pokemon_on_page.setdefault('img_url', request.build_absolute_uri(pokemon.photo.url))
            pokemon_on_page.setdefault('title_ru', pokemon.title)
            pokemon_on_page.setdefault('description', pokemon.description)
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
