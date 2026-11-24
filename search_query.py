import flet
import json
from config import gemini_client
def main(page: flet.Page):
    
    with open("localities.json","r") as f:
        cities_and_localities=json.load(f)
    professional_list=None
    warning_message=None
    results=None
    error_text=flet.Text("",color="red",visible=False)
    select_locality=flet.Dropdown(width=300,label="Select Locality",visible=False)
    select_professional=flet.Dropdown(width=300,label="Select a Professional",visible=False)
    def city_selected(e):
        localities=cities_and_localities[select_city.value]
        select_locality.value=None
        select_professional.value=None
        select_locality.options=[flet.dropdown.Option(locality) for locality in localities]
        select_locality.visible=True
        select_professional.options=[flet.dropdown.Option("Carpenter"),flet.dropdown.Option("Electrician"),flet.dropdown.Option("Plumber")]
        select_professional.visible=True
        page.update()
    def search(e):
        nonlocal professional_list
        nonlocal warning_message
        nonlocal results
        nonlocal error_text
        if not select_city.value:
            error_text.value="Please select a city"
            error_text.visible=True
            page.update()
            return      
        if not select_locality.value:
            error_text.value="Please select a locality"
            error_text.visible=True
            page.update()
            return 
        if not select_professional.value:
            error_text.value="Please select a professional"
            error_text.visible=True
            page.update()
            return 
        error_text.visible = False
        error_text.value = ""
        if professional_list is not None and professional_list in page.controls:
                    page.controls.remove(professional_list)
        if warning_message is not None and warning_message in page.controls:
                page.controls.remove(warning_message)
        if results is not None and results in page.controls:
             page.controls.remove(results)
        spinner=flet.ProgressRing(width=50,height=50)
        
        page.add(spinner)
        page.update()
        client=gemini_client()
        try:
            response=client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[f"""
                        Find a comprehensive list of top-rated {select_professional.value}s in {select_locality.value}, {select_city.value}.
                        Use information from JustDial, Sulekha, IndiaMart and other reputable business directories if available.
                        Return only valid JSON
                        Do not include markdown.
                        Do not include explanations.
                        Do not include code fences.
                        Do not include any text before or after the JSON.
                        JSON format:
                        [
                            {{
                            "Name":"",
                            "Phone":"",
                            "Rating":""
                            }},
                            {{
                            "Name":"",
                            "Phone":"",
                            "Rating":""
                            }}
                        ]
                        Return at least 5 results if available.
                                    """])
        except Exception as ex:
             print("ERROR:", ex)
             if spinner in page.controls:
                  page.controls.remove(spinner)
             error_text.value="Unable to connect to fetch results at the moment.\nPlease try again later."
             error_text.visible=True
             page.update()
             return 
        try:
            output=json.loads(response.text)
            if not isinstance(output, list):
                 if spinner in page.controls:
                    page.controls.remove(spinner)
                 error_text.value="Unexpected response format\nPlease try again later."
                 error_text.visible=True
                 page.update()
                 return
            if not output:
                 if spinner in page.controls:
                      page.controls.remove(spinner)
                 error_text.value="No professionals found"
                 error_text.visible=True
                 page.update()
                 return
        except json.JSONDecodeError:
             if spinner in page.controls:
                page.controls.remove(spinner)
             error_text.value="Unable to process results.\nPlease try again later."
             error_text.visible=True
             page.update()
             return
        rows=[]
        
        for row in output:
            rows.append(flet.DataRow(cells=[
                flet.DataCell(flet.Text(row.get("Name","N/A"))),
                flet.DataCell(flet.Text(row.get("Phone","N/A"))),
                flet.DataCell(flet.Text(row.get("Rating","N/A"))),
            ]))
        professional_list=flet.DataTable(columns=[
             flet.DataColumn(flet.Text("Name")),
             flet.DataColumn(flet.Text("Phone")),
             flet.DataColumn(flet.Text("Rating"))],
             rows=rows
        )
        warning_message=flet.Text("Warning:Some results may be outdated or incorrect. Please verify before use.",color="orange")
        if spinner in page.controls:
            page.controls.remove(spinner)
        results=flet.Container(
             content=flet.Column(
                  controls=[professional_list],
                  scroll=flet.ScrollMode.AUTO
             ),
             height=500
        )
        page.add(results,warning_message)
        if search_professional in page.controls:
             page.controls.remove(search_professional)
        page.update()
    page.horizontal_alignment=flet.CrossAxisAlignment.CENTER
    cities=list(cities_and_localities.keys())
    select_city=flet.Dropdown(width=300,label="Select City",options=[flet.dropdown.Option(city) for city in cities],on_select=city_selected,visible=True)
    search_professional=flet.Text("Search Professional",size=40)
    page.add(search_professional,select_city,select_locality,select_professional,error_text,flet.OutlinedButton("Search",on_click=search))
    