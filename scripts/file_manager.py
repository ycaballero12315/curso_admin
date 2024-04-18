import os
import sys
import json
from subprocess import check_output

class FileManager:
    def __init__(self, directory):
        self.directory = directory
        self.output_dir = os.path.abspath("./resources")

    def execute(self, cant_mb):
        self.validate_directory()
        output_json = os.path.join(self.output_dir, "propietarios.json")
        output_txt = os.path.join(self.output_dir, "archivos_mas_grandes.txt")
        files = self.file_list(cant_mb)
        data = self.file_process(files)
        owner = os.stat(files[0]).st_uid  # Obtener el propietario del primer archivo de la lista
        
        # Verificar y crear directorio de salida si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
            
        self.json_save(data, output_json)
        self.txt_save(files, output_txt, cant_mb, owner)
        print(f"La información se ha guardado en {output_json} (JSON) y {output_txt} (TXT)")

    def show_error(self, msg):
        print("Error:", msg, file=sys.stderr)
        sys.exit(1)

    def get_input(self, prompt, type_func):
        while True:
            try:
                return type_func(input(prompt))
            except ValueError:
                print("Por favor, ingrese un valor válido.")

    def validate_directory(self):
        if not os.path.isdir(self.directory):
            self.show_error("El directorio especificado no existe o no es un directorio.")

    def size_convert(self, size):
        size = int(size)
        if size < 1024:
            return f"{size}B"
        elif size < 1048576:
            return f"{size // 1024}KB"
        elif size < 1073741824:
            return f"{size // 1048576}MB"
        else:
            return f"{size // 1073741824}GB"

    def file_list(self, cant_mb):
        try:
            result = check_output(["find", self.directory, "-type", "f", "-size", f"+{cant_mb}M"]).decode("utf-8").splitlines()
        except Exception as e:
            self.show_error(f"No se pudo listar los archivos: {e}")
        if not result:
            self.show_error(f"No se encontraron archivos mayores a {cant_mb}MB en el directorio: {self.directory}")
        return result

    def file_process(self, files):
        data = []
        for file in files:
            servidor = file.split("server=")[-1].split(",")[0]
            directorio_sin_conexion = file.split("smb-share:server=")[-1].split(",")[-1][2:]
            directorio_sin_archivo = os.path.dirname(directorio_sin_conexion).replace("are=d$", "")
            owner = os.stat(file).st_uid
            size = os.stat(file).st_size
            size_human = self.size_convert(size)
            type = check_output(["file", "-b", "--mime-type", file]).decode("utf-8").strip()
            data.append({
                "archivo": os.path.basename(file),
                "directorio": directorio_sin_archivo,
                "servidor": servidor,
                "propietario": owner,
                "tamaño": size_human,
                "tipo": type
            })
        return data

    def json_save(self, data, output_file):
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.show_error(f"No se pudo escribir en el archivo JSON: {e}")

    def txt_save(self, files, output_file, cant_mb, owner):
        try:
            with open(output_file, "w") as f:
                f.write(f"Los archivos mayores a {cant_mb} MB en {self.directory} son:\n")
                for file in files:
                    size = os.stat(file).st_size
                    size_human = self.size_convert(size)
                    type = check_output(["file", "-b", "--mime-type", file]).decode("utf-8").strip()
                    f.write(f"Archivo: {os.path.basename(file)} - Propietario: {owner} - Tamaño: {size_human} - Tipo: {type}\n")
        except Exception as e:
            self.show_error(f"No se pudo escribir en el archivo TXT: {e}")


