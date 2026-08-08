import matplotlib.pyplot as plt
import numpy as np

def configurar_graficos():
    fig = plt.figure(figsize=(15, 7))
    
    # Gráfico 3D (Espacial com Planos)
    ax_3d = fig.add_subplot(121, projection='3d')
    ax_3d.set_title("Representação Espacial 3D")
    ax_3d.set_xlabel("X (Abcissa)")
    ax_3d.set_ylabel("Y (Afastamento)")
    ax_3d.set_zlabel("Z (Cota)")
    ax_3d.set_xlim([-10, 15])
    ax_3d.set_ylim([-10, 15])
    ax_3d.set_zlim([-10, 15])
    
    # Planos PV e PH transparentes
    xx = np.linspace(-10, 10, 10)
    zz = np.linspace(-10, 10, 10)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)
    ax_3d.plot_surface(XX, YY, ZZ, color='gray', alpha=0.15, edgecolor='none')
    
    XX_h, YY_h = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
    ZZ_h = np.zeros_like(XX_h)
    ax_3d.plot_surface(XX_h, YY_h, ZZ_h, color='gray', alpha=0.15, edgecolor='none')
    ax_3d.plot([-10, 10], [0, 0], [0, 0], color='black', linewidth=2, label="Linha de Terra")

    # Gráfico 2D (Épura)
    ax_2d = fig.add_subplot(122)
    ax_2d.set_title("Épura (2D)")
    ax_2d.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax_2d.set_xlabel("X (Abcissa)")
    ax_2d.set_ylabel("Projeções")
    ax_2d.set_xlim([-10, 15])
    ax_2d.set_ylim([-10, 15])
    ax_2d.grid(True, linestyle='--', alpha=0.5)
    
    return fig, ax_3d, ax_2d

def plotar_ponto(ax_3d, ax_2d, nome, x, y, z):
    # 3D
    ax_3d.scatter(x, y, z, color='black', s=40)
    ax_3d.text(x, y, z, f" ({nome})", fontsize=10, fontweight='bold')
    ax_3d.scatter(x, 0, z, color='blue', s=30)
    ax_3d.scatter(x, y, 0, color='green', s=30)
    ax_3d.plot([x, x], [y, y], [0, z], color='gray', linestyle='--', alpha=0.5)
    ax_3d.plot([x, x], [0, y], [z, z], color='gray', linestyle='--', alpha=0.5)

    # Épura 2D
    ax_2d.scatter(x, z, color='blue', s=40)
    ax_2d.text(x, z + 0.3, f"{nome}'", fontsize=10, color='blue', fontweight='bold')
    ax_2d.scatter(x, -y, color='green', s=40)
    ax_2d.text(x, -y - 0.5, f"{nome}''", fontsize=10, color='green', fontweight='bold')
    ax_2d.plot([x, x], [-y, z], color='gray', linestyle=':')

def modulo_pontos():
    print("\n--- MÓDULO: PONTOS ---")
    pontos = {}
    while True:
        nome = input("Nome do ponto (ex: A, B...) ou 'ok' para gerar: ").strip().upper()
        if nome == 'OK' or not nome: break
        try:
            x = float(input(f"Abcissa (X) de {nome}: "))
            y = float(input(f"Afastamento (Y) de {nome}: "))
            z = float(input(f"Cota (Z) de {nome}: "))
            pontos[nome] = (x, y, z)
        except ValueError: print("Digite apenas números válidos.")
            
    if not pontos: return
    fig, ax_3d, ax_2d = configurar_graficos()
    for nome, (x, y, z) in pontos.items():
        plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
    plt.tight_layout()
    plt.show()

def modulo_retas():
    print("\n--- MÓDULO: RETAS ---")
    pontos = {}
    print("Cadastre os pontos que compõem as retas:")
    while True:
        nome = input("Nome do ponto (ex: A, B...) ou 'ok' para avançar: ").strip().upper()
        if nome == 'OK' or not nome: break
        try:
            x = float(input(f"Abcissa (X) de {nome}: "))
            y = float(input(f"Afastamento (Y) de {nome}: "))
            z = float(input(f"Cota (Z) de {nome}: "))
            pontos[nome] = (x, y, z)
        except ValueError: print("Digite apenas números válidos.")
            
    if len(pontos) < 2:
        print("Cadastre pelo menos 2 pontos.")
        return
        
    lista_nomes = list(pontos.keys())
    fig, ax_3d, ax_2d = configurar_graficos()
    for nome, (x, y, z) in pontos.items():
        plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
        
    for i in range(len(lista_nomes) - 1):
        p1, p2 = pontos[lista_nomes[i]], pontos[lista_nomes[i+1]]
        ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linewidth=2)
        ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linewidth=1.2)
        ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linewidth=1.2)
        
    plt.tight_layout()
    plt.show()

def modulo_solidos():
    print("\n==================================================")
    print("      📐 MÓDULO: SÓLIDOS (PRISMAS, PIRÂMIDES, CONES) ")
    print("==================================================")
    print("[1] Inserir base poligonal manualmente")
    print("[2] Gerar Base Regular automática a partir de A e B (Ex: Hexágono/Quadrado)")
    print("[3] Cone / Cilindro (Base Circular por Centro e Raio)")
    
    modo = input("\nEscolha a opção (1, 2 ou 3): ").strip()
    pontos = {}
    
    if modo == '3':
        print("\n--- MÓDULO DE CORPO REDONDO (CONE / CILINDRO) ---")
        try:
            ox = float(input("Abcissa (X) do Centro da Base (O): "))
            oy = float(input("Afastamento (Y) do Centro da Base (O): "))
            oz = float(input("Cota (Z) do Centro da Base (O): "))
            pontos['O'] = (ox, oy, oz)
            
            raio = float(input("Raio da base: "))
            altura = float(input("Altura do sólido: "))
            
            tipo_redondo = input("É [1] Cilindro ou [2] Cone? ").strip()
            
            fig, ax_3d, ax_2d = configurar_graficos()
            plotar_ponto(ax_3d, ax_2d, 'O', ox, oy, oz)
            
            # Gerar círculo da base e do topo por amostragem trigonométrica
            theta = np.linspace(0, 2 * np.pi, 30)
            base_x = ox + raio * np.cos(theta)
            base_y = oy + raio * np.sin(theta)
            base_z = np.full_like(theta, oz)
            
            topo_z = np.full_like(theta, oz + altura)
            
            # Plotar base 3D e 2D
            ax_3d.plot(base_x, base_y, base_z, color='purple', linewidth=2, label="Base Inferior")
            ax_2d.plot(base_x, base_z, color='blue', linewidth=1.2)
            ax_2d.plot(base_x, -base_y, color='green', linewidth=1.2)
            
            if tipo_redondo == '1': # Cilindro
                ax_3d.plot(base_x, base_y, topo_z, color='purple', linewidth=2, label="Base Superior")
                ax_2d.plot(base_x, topo_z, color='blue', linewidth=1.2)
                ax_2d.plot(base_x, -base_y, color='green', linewidth=1.2)
                # Geratrizes laterais representativas
                for i in [0, 7, 15, 22]:
                    ax_3d.plot([base_x[i], base_x[i]], [base_y[i], base_y[i]], [base_z[i], topo_z[i]], color='purple', linestyle='--')
                    ax_2d.plot([base_x[i], base_x[i]], [base_z[i], topo_z[i]], color='blue', linestyle='--')
                    ax_2d.plot([base_x[i], base_x[i]], [-base_y[i], -base_y[i]], color='green', linestyle='--')
            else: # Cone
                vx, vy, vz = ox, oy, oz + altura
                plotar_ponto(ax_3d, ax_2d, 'V', vx, vy, vz)
                for i in [0, 7, 15, 22]:
                    ax_3d.plot([base_x[i], vx], [base_y[i], vy], [base_z[i], vz], color='purple', linestyle='--')
                    ax_2d.plot([base_x[i], vx], [base_z[i], vz], color='blue', linestyle='--')
                    ax_2d.plot([base_x[i], vx], [-base_y[i], -vy], color='green', linestyle='--')
            
            plt.tight_layout()
            plt.show()
            return
        except Exception as e:
            print(f"Erro ao gerar corpo redondo: {e}")
            return

    if modo == '2':
        print("\n--- GERADOR DE BASE REGULAR POR 2 PONTOS ---")
        try:
            ax = float(input("Abcissa (X) do ponto A: "))
            ay = float(input("Afastamento (Y) do ponto A: "))
            az = float(input("Cota (Z) do ponto A: "))
            
            bx = float(input("Abcissa (X) do ponto B: "))
            by = float(input("Afastamento (Y) do ponto B: "))
            bz = float(input("Cota (Z) do ponto B: "))
            
            pontos['A'] = (ax, ay, az)
            pontos['B'] = (bx, by, bz)
            
            lados = int(input("Número total de lados da base (ex: 3 para triângulo, 4 para quadrado, 6 para hexágono): "))
            
            v_x = bx - ax
            v_y = by - ay
            lado_tam = np.hypot(v_x, v_y)
            
            angulo_interno = (lados - 2) * np.pi / lados
            angulo_rot_externo = np.pi - angulo_interno
            
            nomes_vert = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            curr_x, curr_y = bx, by
            angulo_atual = np.arctan2(v_y, v_x)
            
            for i in range(2, lados):
                angulo_atual += angulo_rot_externo
                curr_x += lado_tam * np.cos(angulo_atual)
                curr_y += lado_tam * np.sin(angulo_atual)
                nome_p = nomes_vert[i]
                pontos[nome_p] = (curr_x, curr_y, az)
                
        except Exception as e:
            print(f"Erro ao gerar base automática: {e}")
            return
    else:
        while True:
            nome = input("Nome do ponto da base (ex: A, B...) ou 'ok' para avançar: ").strip().upper()
            if nome == 'OK' or not nome: break
            try:
                x = float(input(f"X de {nome}: "))
                y = float(input(f"Y de {nome}: "))
                z = float(input(f"Z de {nome}: "))
                pontos[nome] = (x, y, z)
            except ValueError: print("Erro.")

    base_nomes = list(pontos.keys())
    if not base_nomes: return

    print("\n[1] Prisma (Reto)")
    print("[2] Pirâmide (Com Vértice no Topo)")
    escolha_sol = input("Escolha o tipo de sólido (1 ou 2): ").strip()

    topo_nomes = []
    if escolha_sol == '1':
        possui_topo = input("Deseja informar a altura para gerar o topo automaticamente? (s/n): ").strip().lower()
        if possui_topo == 's':
            try:
                altura = float(input("Digite a altura do prisma: "))
                for original in base_nomes:
                    px, py, pz = pontos[original]
                    t_nome = f"{original}'"
                    pontos[t_nome] = (px, py, pz + altura)
                    topo_nomes.append(t_nome)
            except ValueError:
                print("Altura inválida.")
        else:
            print(f"\nCadastre os pontos da Base Superior (Topo) correspondentes:")
            for original in base_nomes:
                t_nome = f"{original}'"
                try:
                    print(f"Para o topo correspondente a {original}:")
                    x = float(input(f"X: "))
                    y = float(input(f"Y: "))
                    z = float(input(f"Z: "))
                    pontos[t_nome] = (x, y, z)
                    topo_nomes.append(t_nome)
                except ValueError:
                    print("Erro nos dados.")
                    return
    elif escolha_sol == '2':
        try:
            print("\nCadastre o Vértice Superior da Pirâmide (V):")
            vx = float(input("X do Vértice V: "))
            vy = float(input("Y do Vértice V: "))
            vz = float(input("Z do Vértice V: "))
            pontos['V'] = (vx, vy, vz)
        except ValueError:
            print("Erro no vértice.")
            return

    fig, ax_3d, ax_2d = configurar_graficos()
    
    for nome, (x, y, z) in pontos.items():
        plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
        
    # Desenhar Base Inferior fechada
    for i in range(len(base_nomes)):
        p1, p2 = pontos[base_nomes[i]], pontos[base_nomes[(i+1)%len(base_nomes)]]
        ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linewidth=2)
        ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linewidth=1.2)
        ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linewidth=1.2)

    # Desenhar Topo e Arestas Laterais do Prisma
    if topo_nomes:
        for i in range(len(topo_nomes)):
            p1, p2 = pontos[topo_nomes[i]], pontos[topo_nomes[(i+1)%len(topo_nomes)]]
            ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linewidth=2)
            ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linewidth=1.2)
            ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linewidth=1.2)
            
        for i in range(len(base_nomes)):
            p1, p2 = pontos[base_nomes[i]], pontos[topo_nomes[i]]
            ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linestyle='--')
            ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linestyle='--')
            ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linestyle='--')
            
    elif 'V' in pontos:
        # Arestas da Pirâmide ligando a base até o Vértice V
        v_coord = pontos['V']
        for b_nome in base_nomes:
            b_coord = pontos[b_nome]
            ax_3d.plot([b_coord[0], v_coord[0]], [b_coord[1], v_coord[1]], [b_coord[2], v_coord[2]], color='purple', linestyle='--')
            ax_2d.plot([b_coord[0], v_coord[0]], [b_coord[2], v_coord[2]], color='blue', linestyle='--')
            ax_2d.plot([b_coord[0], v_coord[0]], [-b_coord[1], -v_coord[1]], color='green', linestyle='--')

    plt.tight_layout()
    plt.show()

# --- TELA INICIAL DO APLICATIVO ---
def main():
    while True:
        print("\n==================================================")
        print("          🚀 GD EM MÃOS - UEFS 🚀                ")
        print("    Geometria Descritiva 3D e Épura Interativa     ")
        print("==================================================")
        print("[1] PONTOS (Estudo do Ponto)")
        print("[2] RETAS (Estudo das Retas e Perfil)")
        print("[3] SÓLIDOS (Prismas, Pirâmides, Cones e Cilindros)")
        print("[0] SAIR")
        
        opcao = input("\nEscolha o assunto desejado (1, 2, 3 ou 0): ").strip()
        
        if opcao == '1':
            modulo_pontos()
        elif opcao == '2':
            modulo_retas()
        elif opcao == '3':
            modulo_solidos()
        elif opcao == '0':
            print("\nEncerrando o GD EM MÃOS. Bons estudos para as pranchas!")
            break
        else:
            print("\nOpção inválida! Escolha 1, 2, 3 ou 0.")

if __name__ == "__main__":
    main()