import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(
    page_title="GD em Mãos - UEFS",
    page_icon="📐",
    layout="wide"
)

def configurar_graficos():
    fig = plt.figure(figsize=(14, 6))
    
    # Gráfico 3D (Espacial com Planos)
    ax_3d = fig.add_subplot(121, projection='3d')
    ax_3d.set_title("Representação Espacial 3D", fontsize=12, fontweight='bold')
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
    ax_2d.set_title("Épura (2D)", fontsize=12, fontweight='bold')
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

def main():
    st.title("🚀 GD EM MÃOS - UEFS 🚀")
    st.subheader("Geometria Descritiva 3D e Épura Interativa")
    st.markdown("---")

    # Menu lateral no Streamlit
    st.sidebar.header("Painel de Controle")
    modulo = st.sidebar.selectbox(
        "Escolha o assunto desejado:",
        ["Pontos (Estudo do Ponto)", "Retas (Estudo das Retas)", "Sólidos (Prismas, Pirâmides, Cones, Cilindros)"]
    )

    if "Pontos" in modulo:
        st.header("📍 Módulo: Pontos")
        num_pontos = st.sidebar.number_input("Quantos pontos deseja cadastrar?", min_value=1, max_value=10, value=2)
        
        pontos = {}
        with st.form("form_pontos"):
            for i in range(int(num_pontos)):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    nome = st.text_input(f"Nome {i+1}", value=chr(65+i))
                with col2:
                    x = st.number_input(f"X ({nome})", value=float(i*2))
                with col3:
                    y = st.number_input(f"Y ({nome})", value=float(i+2))
                with col4:
                    z = st.number_input(f"Z ({nome})", value=float(i+1))
                if nome:
                    pontos[nome.strip().upper()] = (x, y, z)
            
            submitted = st.form_submit_button("Gerar Visualização")
            
        if submitted and pontos:
            fig, ax_3d, ax_2d = configurar_graficos()
            for nome, (x, y, z) in pontos.items():
                plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
            plt.tight_layout()
            st.pyplot(fig)

    elif "Retas" in modulo:
        st.header("📏 Módulo: Retas")
        num_pontos_retas = st.sidebar.number_input("Número de pontos para compor a reta", min_value=2, max_value=10, value=2)
        
        pontos = {}
        with st.form("form_retas"):
            for i in range(int(num_pontos_retas)):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    nome = st.text_input(f"Ponto {i+1}", value=chr(65+i))
                with col2:
                    x = st.number_input(f"X ({nome})", value=float(i*3))
                with col3:
                    y = st.number_input(f"Y ({nome})", value=float(i+1))
                with col4:
                    z = st.number_input(f"Z ({nome})", value=float(i+2))
                if nome:
                    pontos[nome.strip().upper()] = (x, y, z)
            
            submitted = st.form_submit_button("Gerar Reta")
            
        if submitted and len(pontos) >= 2:
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
            st.pyplot(fig)

    elif "Sólidos" in modulo:
        st.header("📐 Módulo: Sólidos")
        tipo_solido = st.radio("Escolha o tipo:", ["Corpo Redondo (Cone / Cilindro)", "Prisma ou Pirâmide (Base Poligonal)"])
        
        if "Corpo Redondo" in tipo_solido:
            st.subheader("Cone / Cilindro")
            col1, col2, col3 = st.columns(3)
            with col1:
                ox = st.number_input("X do Centro (O)", value=0.0)
            with col2:
                oy = st.number_input("Y do Centro (O)", value=3.0)
            with col3:
                oz = st.number_input("Z do Centro (O)", value=2.0)
                
            col4, col5, col6 = st.columns(3)
            with col4:
                raio = st.number_input("Raio da base", value=3.0)
            with col5:
                altura = st.number_input("Altura do sólido", value=5.0)
            with col6:
                tipo_redondo = st.selectbox("Forma", ["Cilindro", "Cone"])
                
            if st.button("Gerar Corpo Redondo"):
                fig, ax_3d, ax_2d = configurar_graficos()
                plotar_ponto(ax_3d, ax_2d, 'O', ox, oy, oz)
                
                theta = np.linspace(0, 2 * np.pi, 30)
                base_x = ox + raio * np.cos(theta)
                base_y = oy + raio * np.sin(theta)
                base_z = np.full_like(theta, oz)
                topo_z = np.full_like(theta, oz + altura)
                
                ax_3d.plot(base_x, base_y, base_z, color='purple', linewidth=2)
                ax_2d.plot(base_x, base_z, color='blue', linewidth=1.2)
                ax_2d.plot(base_x, -base_y, color='green', linewidth=1.2)
                
                if tipo_redondo == "Cilindro":
                    ax_3d.plot(base_x, base_y, topo_z, color='purple', linewidth=2)
                    ax_2d.plot(base_x, topo_z, color='blue', linewidth=1.2)
                    ax_2d.plot(base_x, -base_y, color='green', linewidth=1.2)
                    for i in [0, 7, 15, 22]:
                        ax_3d.plot([base_x[i], base_x[i]], [base_y[i], base_y[i]], [base_z[i], topo_z[i]], color='purple', linestyle='--')
                        ax_2d.plot([base_x[i], base_x[i]], [base_z[i], topo_z[i]], color='blue', linestyle='--')
                        ax_2d.plot([base_x[i], base_x[i]], [-base_y[i], -base_y[i]], color='green', linestyle='--')
                else:
                    vx, vy, vz = ox, oy, oz + altura
                    plotar_ponto(ax_3d, ax_2d, 'V', vx, vy, vz)
                    for i in [0, 7, 15, 22]:
                        ax_3d.plot([base_x[i], vx], [base_y[i], vy], [base_z[i], vz], color='purple', linestyle='--')
                        ax_2d.plot([base_x[i], vx], [base_z[i], vz], color='blue', linestyle='--')
                        ax_2d.plot([base_x[i], vx], [-base_y[i], -vy], color='green', linestyle='--')
                
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.info("Para prismas e pirâmides, utilize a estrutura padrão adaptada por formulários dinâmicos.")

if __name__ == "__main__":
    main()
