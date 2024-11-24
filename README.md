# 🩻 **Simulação de Mecanismo por Trás de Tomógrafos de Luz**  

## 📘 **Descrição do Projeto**  
Este projeto foi desenvolvido como parte do trabalho final da disciplina de **Física Elétrica**, no curso de **Engenharia de Computação**. O objetivo foi simular um dos mecanismos essenciais no funcionamento de **tomógrafos de luz**, utilizando:  
- 🐍 **Python**  
- 📚 **Bibliotecas matemáticas**  
- 🧮 Conceitos como **Transformada de Radon**  

---

## 🛠️ **Etapas do Desenvolvimento**  

### 1️⃣ **Tratamento de Imagens**  
- Os professores forneceram **2.999 imagens**, que passaram por:  
  - **Recortes e adaptações**  
  - Organização em **31 sinogramas**

### 2️⃣ **Aplicação da Transformada de Radon**  
A Transformada de Radon é uma ferramenta matemática que transforma uma função bidimensional (no caso, uma imagem) em um conjunto de suas projeções ao longo de linhas retas em diferentes ângulos., utilizada em:  
- **Reconstrução de imagens médicas, com ênfase em Tomografia Computadorizada.**  
- Mapeamento de uma imagem 2D para o espaço de projeções em todas as direções


---

## 💻 **Implementação em Python**  
### 🖼️ **Passos principais do projeto**  
1. **Carregamento das imagens**
2. **Recorte e rotação**
3. **Conversão para escala de cinza**
4. **Criação de sinogramas**
5. **Aplicação da Transformada de Radon**  
6. **Empilhamento de dados**  
7. **Visualização final**  

---

## 📊 **Conceitos Matemáticos Utilizados**  
A **Transformada de Radon** transforma uma imagem 2D \( f(x, y) \) em um conjunto de projeções:  
- Cada projeção integra a função ao longo de uma linha reta em uma direção específica.  
Para recuperar a imagem original \( f(x, y) \), utilizamos a **Transformada Inversa de Radon**.  

---
