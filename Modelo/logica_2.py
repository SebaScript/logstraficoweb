from collections import Counter


class AnalizadorLogs:

    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo

    def procesar_logs(self) -> dict[str, any]:
        total_solicitudes = 0
        solicitud_metodo = 0

        with open(self.nombre_archivo, "r", encoding= "utf-8") as archivo:
            lineas = archivo.readlines()

            solicitudes = []
            solicitud = {}
            for linea in lineas:
                if linea.startswith('Dirección IP:'):
                    total_solicitudes += 1
                elif linea.startswith('Método: HTTP'):
                    solicitud_metodo += 1
                elif linea.startswith('URL:'):
                    solicitud['url'] = linea.split(':')[1].strip()
                elif linea.startswith('Código de respuesta:'):
                    solicitud['codigo de respuesta'] = int(linea.split(':')[1].strip())
                elif linea.startswith('Tamaño de respuesta:'):
                    solicitud['tamaño de respuesta'] = int(linea.split(':')[1].strip())
                    solicitudes.append(solicitud)

            codigos_respuesta = [solicitud['codigo de respuesta'] for solicitud in solicitudes]
            tamano_total_respuesta = sum([solicitud['tamaño de respuesta'] for solicitud in solicitudes])
            tamano_promedio_respuesta = tamano_total_respuesta / total_solicitudes if total_solicitudes > 0 else 0
            contador_urls = Counter([solicitud['url'] for solicitud in solicitudes]).most_common(10)

            informe = {
                'total solicitudes': total_solicitudes,
                'solicitudes metodo': solicitud_metodo,
                'codigo respuesta': codigos_respuesta,
                'tamaño_total_respuesta': tamano_total_respuesta,
                'tamaño_promedio_respuesta': tamano_promedio_respuesta,
                'top_10_urls': contador_urls,
            }

            return informe


analizador = AnalizadorLogs('trafico_web.log')
informe = analizador.procesar_logs()
print(informe)