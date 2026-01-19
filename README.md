# 🐍 Snake Dungeon Crawler

Um jogo de exploração de masmorras procedural desenvolvido com **Python** e **Pygame Zero**.  
O projeto combina a mecânica clássica de movimentação da *“cobrinha”* com a exploração de mapas gerados aleatoriamente, onde o jogador deve encontrar a saída enquanto sobrevive a inimigos rítmicos.

---

## 🚀 Funcionalidades

- **Geração Procedural de Mapas**  
  Algoritmo que cria layouts únicos de salas e corredores a cada novo nível, garantindo que nenhum jogo seja igual ao anterior.

- **Sistema de Colisão Inteligente**  
  Verificação matemática rigorosa para garantir que as salas não se sobreponham e que o caminho seja sempre navegável.

- **Dificuldade Progressiva**  
  A cada nível superado, a quantidade de inimigos aumenta, exigindo mais estratégia e reflexos do jogador.

- **Movimentação Cadenciada**  
  Inimigos movidos por um sistema de tempo independente (`clock.schedule_interval`), criando um padrão de movimento estratégico.

---

## 🛠️ Lógica de Programação Aplicada

### 1. Geração de Salas e Corredores

- O mapa é tratado como uma **matriz bidimensional**, onde:
  - `1` representa parede
  - `0` representa chão

- **Validação de Espaço**  
  Antes de *“cavar”* uma sala, o código consulta a `rooms_list`.  
  - Se houver colisão detectada, o comando `break` interrompe a checagem.
  - O `continue` descarta a tentativa inválida.

- **Conexão de Centros**  
  O código identifica o centro geométrico de cada sala através da fórmula:
  pos + dimensão // 2

  
Em seguida, cava túneis em formato de **“L”** (horizontal seguido de vertical), assegurando a conectividade total do mapa.

---

### 2. Controle de Inimigos (Spawn & Ritmo)

Os inimigos são posicionados via um loop `while True` que valida três condições essenciais antes de confirmar o *spawn*:

- A célula do mapa deve ser chão (`dungeon_map == 0`).
- A posição não pode coincidir com nenhum segmento do herói (`hero_segments`).
- A posição não pode obstruir o portal de saída (`exit_portal`).

O movimento rítmico é gerenciado pelo relógio interno:

# O movimento rítmico é gerenciado pelo relógio interno do Pygame Zero:
clock.schedule_interval(update_enemies, 0.6)

### 3. Gerenciamento de Estados e Input

- Botão Play 
- **Utiliza button_play.collidepoint(pos) para detectar cliques do mouse no menu, onde pos representa as coordenadas (x, y) do cursor.

- Reset com Space
- **Implementação da tecla Espaço (keys.SPACE) para reiniciar o jogo instantaneamente após um Game Over ou durante o menu, limpando as listas e regenerando o ambiente.

| Comando           | Ação                                   |
| ----------------- | -------------------------------------- |
| Setas Direcionais | Movimentam a cobra pela dungeon        |
| Mouse (Clique)    | Interage com os botões do menu inicial |
| Space (Espaço)    | Reinicia o jogo (Reset) após a derrota |

📦Como rodar o projeto

- Certifique-se de ter o Python instalado.

- Instale a biblioteca Pygame Zero:

- pip install pgzero


- Clone este repositório:

- git clone https://github.com/seu-usuario/snake-dungeon-crawler.git


## 4. Execute o jogo:

- pgzrun nome_do_seu_arquivo.py

📝 Aprendizados Técnicos

- Manipulação de coordenadas e matrizes para criação de conteúdo procedural.

- Uso de sistemas de agendamento de tarefas (clocks) para eventos rítmicos.

- Lógica de colisões em grades e tratamento de eventos de teclado e mouse.

