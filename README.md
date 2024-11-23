* Foi proposto aos estudantes, como projeto final da disciplina de Física Elétrica, do curso de Engenharia de Computação, a simulação de um dos mecanismos por trás de tomógrafos de luz. 

* Para isto, o meio para o desenvolvimento de tal projeto é a linguagem Python, o uso de suas bibliotecas, e conceitos matemáticos focados em relação à Transformada de Radon.

1. Recebimento dos arquivos: Os professores realizaram o envio das 2999 imagens, a fim de que estas pudessem ser tratadas, para assim, dar início ao projeto.
2. Ao finalizar o tratamento das imagens (Recortes e adaptações), elas foram organizadas em 31 Sinogramas (último com uma imagem a menos).
3. Com os sinogramas prontos, foi necessário aplicar a Transformada de Radon, que consiste em uma técnica matemática usada em processamento de imagens, que desempenha um papel crucial em tomografias computadorizadas
e reconstrução de imagens médicas. Ela mapeia uma função definida em um espaço 2D (como uma imagem) para o espaço das suas projeções em todas as direções.

* Ou seja, a Transformada de Radon transforma uma imagem 2D f(𝑥,𝑦) em um conjunto de projeções, onde cada projeção representa a integral da função ao longo de uma linha reta em uma dada direção.
A Transformada de Radon de uma função 

* Para recuperar a imagem original  𝑓(𝑥,𝑦), utiliza-se a Transformada Inversa de Radon. Realizada por meio de métodos iterativos.

4. Em Python:

* Carregar Imagens:


* Conversão para Escala de Cinza:


* Transformada de Radon:


* Empilhamento:


* Visualização:



