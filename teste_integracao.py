from medias_wrapper import calcular_media_final_c, C_DISPONIVEL

if C_DISPONIVEL:
    print("✅ Biblioteca C carregada com sucesso!")
    
    # Teste simples
    respostas_teste = [
        {"nota": 8.0}, {"nota": 7.5}, {"nota": 9.0}
    ]
    
    resultado = calcular_media_final_c("teste", respostas_teste)
    print("Resultado do cálculo em C:")
    print(f"Média Final: {resultado['media_final']}")
    print(f"Status: {resultado['status']}")
else:
    print("❌ Biblioteca C não disponível")
