import folium
import geopandas as gpd
import pandas as pd

class GeoMap:
    """Конструктор, создает объект карты
    input:координаты центра карты (значения долготы и широты)    
    """

    def __init__(self, x_centre, y_centre):
        self.geo_map = folium.Map(location=[x_centre,y_centre],
                                    zoom_start=9,
                                    tiles=None)
        folium.TileLayer('CartoDB positron',
                        name="Light Map",
                        control=False).add_to(self.geo_map)
    

    """Размечает карту на задаваемые области
    input:for_geo_data - geojson файл (или geopandas frame)
        for_data - итоговый датафрейм
        for columns - колонки, которые будут задействованы в работе
        for_key_on - по какой колонке будет происходить "схлестывание"
        for_legend - легенда карты
    """
    def create_coropleth(self,
                        for_geo_data,
                        for_data,
                        for_columns,
                        for_key_on,
                        for_legend):

        folium.Choropleth(geo_data=for_geo_data,name='choropleth',
                        data=for_data,columns=for_columns,
                        key_on=for_key_on,fill_color='YlGnBu',
                        fill_opacity=0.9,line_opacity=0.2,
                        legend_name=for_legend
                        ).add_to(self.geo_map)


    """Добавляет информацию на карту
    input:  df - датафрейм с данными
            info_columns - список колонок для отображения информации
            labels - список подписей к информации из колонок
    """

    def add_info_on_map(self,df, info_columns,labels):
        style_function = lambda x:{'fillColor':'#ffffff',
                                    'color':'#000000',
                                    'fillOpacity':0.1,
                                    'weight':0.1}
        css=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        folium_tooltip = folium.features.GeoJsonTooltip(
                                            fields = info_columns,
                                            aliases = labels,
                                            style = css)
        SuburbInfo = folium.features.GeoJson(
                                            df,
                                            style_function=style_function,
                                            control=False,
                                            tooltip = folium_tooltip)
        self.geo_map.add_child(SuburbInfo)
        self.geo_map.keep_in_front(SuburbInfo)
        folium.LayerControl().add_to(self.geo_map)