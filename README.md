# 🩻 **Simulação de Mecanismo por Trás de Tomógrafos de Luz**  

## 📘 **Descrição do Projeto**  
Este projeto foi desenvolvido como parte do trabalho final da disciplina de **Física Elétrica**, no curso de **Engenharia de Computação**. O objetivo foi simular um dos mecanismos essenciais no funcionamento de **tomógrafos de luz**, utilizando:  
- 🐍 **Python**  
- 📚 Suas **bibliotecas matemáticas**  
- 🧮 Conceitos como a **Transformada de Radon**  

---

## 🛠️ **Etapas do Desenvolvimento**  

### 1️⃣ **Recebimento e Tratamento de Imagens**  
- Os professores forneceram **2.999 imagens**, que passaram por:  
  - **Recortes e adaptações**  
  - Organização em **31 sinogramas** (o último com uma imagem a menos)  

### 2️⃣ **Aplicação da Transformada de Radon**  
A **Transformada de Radon** é uma técnica essencial em processamento de imagens, utilizada na:  
- **Reconstrução de imagens médicas**  
- Mapeamento de uma imagem 2D para o espaço de projeções em todas as direções  

### 🔄 **Transformada Inversa de Radon**  
Para reconstruir a imagem original, utilizou-se a **Transformada Inversa de Radon**, implementada com:  
- **Métodos iterativos** em Python  

---

## 💻 **Implementação em Python**  
### 🖼️ **Passos principais do projeto**  
1. **Carregamento das imagens**  
2. **Conversão para escala de cinza**  
3. **Aplicação da Transformada de Radon**  
4. **Empilhamento de dados**  
5. **Visualização final**  

---

## 📊 **Conceitos Matemáticos Utilizados**  
A **Transformada de Radon** transforma uma imagem 2D \( f(x, y) \) em um conjunto de projeções:  
- Cada projeção é a integral da função ao longo de uma linha reta em uma direção específica  
Para recuperar a imagem original \( f(x, y) \), utilizamos a **Transformada Inversa de Radon**.  

---
