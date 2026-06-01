import ctypes
import os
from typing import List, Dict, Any

# Definir a estrutura para o resultado
class ResultadoMedia(ctypes.Structure):
    _fields_ = [
        ("media_atividades", ctypes.c_double),
        ("nota_np1", ctypes.c_double),
        ("nota_np2", ctypes.c_double),
        ("media_final", ctypes.c_double),
        ("status", ctypes.c_char * 20)
    ]

def carregar_biblioteca_c():
    """Carrega a biblioteca C compilada"""
    dll_path = os.path.join(os.path.dirname(__file__), "calculo_medias.dll")
    
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"Biblioteca C não encontrada: {dll_path}")
    
    lib = ctypes.CDLL(dll_path)
    
    # Configurar a função principal
    lib.calcular_media_final_c.argtypes = [
        ctypes.POINTER(ctypes.c_double),  # notas_atividades
        ctypes.c_int,                     # num_atividades
        ctypes.c_double,                  # nota_np1
        ctypes.c_double                   # nota_np2
    ]
    lib.calcular_media_final_c.restype = ResultadoMedia
    
    return lib

# Carregar biblioteca (pode falhar silenciosamente)
try:
    lib_calculo = carregar_biblioteca_c()
    C_DISPONIVEL = True
except (FileNotFoundError, OSError):
    lib_calculo = None
    C_DISPONIVEL = False
    print("Aviso: Biblioteca C não disponível. Usando versão Python.")

def calcular_media_final_c(aluno_id: str, respostas: List[Dict[str, Any]]):
    """Versão em C do cálculo de média final"""
    if not C_DISPONIVEL:
        # Fallback para Python puro
        from PIM_final import calcular_media_final_python
        return calcular_media_final_python(aluno_id, respostas)
    
    # Extrair notas das atividades
    notas_atividades = [float(r.get("nota", 0)) for r in respostas if r.get("nota") is not None]
    
    # Converter para array C
    num_atividades = len(notas_atividades)
    if num_atividades > 0:
        notas_array = (ctypes.c_double * num_atividades)(*notas_atividades)
    else:
        notas_array = (ctypes.c_double * 1)(0.0)
        num_atividades = 1
    
    # Obter notas das provas (simuladas para exemplo)
    # Você precisará adaptar esta parte para seu código real
    nota_np1 = 7.5  # Exemplo - substitua pela lógica real
    nota_np2 = 8.0  # Exemplo - substitua pela lógica real
    
    # Chamar função C
    resultado_c = lib_calculo.calcular_media_final_c(
        notas_array, num_atividades, nota_np1, nota_np2
    )
    
    # Converter resultado para dicionário Python
    return {
        "media_atividades": float(resultado_c.media_atividades),
        "nota_np1": float(resultado_c.nota_np1),
        "nota_np2": float(resultado_c.nota_np2),
        "media_final": float(resultado_c.media_final),
        "status": resultado_c.status.decode('utf-8')
    }

# Versão fallback em Python puro
def calcular_media_final_python(aluno_id: str, respostas: List[Dict[str, Any]]):
    """Versão Python puro (fallback)"""
    notas_atividades = [r.get("nota") for r in respostas if r.get("nota") is not None]
    media_atividades = sum(notas_atividades) / len(notas_atividades) if notas_atividades else 0
    
    # Notas de exemplo - substitua pela sua lógica real
    nota_np1 = 7.5
    nota_np2 = 8.0
    
    media_final = (nota_np1 * 4 + nota_np2 * 4 + media_atividades * 2) / 10
    
    return {
        "media_atividades": media_atividades,
        "nota_np1": nota_np1,
        "nota_np2": nota_np2,
        "media_final": media_final,
        "status": "Aprovado" if media_final >= 7 else "Reprovado"
    }
