import json
import csv
import re
import random

# Função para gerar as tags no formato IOB
def generate_iob_tags(tokens, entities):
    tags = ['O'] * len(tokens)  # Inicializa todas as tags como 'O'
    
    for start, end, label in entities:
        entity_started = False
        for i, (token, token_start, token_end) in enumerate(tokens):
            if token_start >= start and token_end <= end:
                if not entity_started:
                    tags[i] = f'B-{label}'  # Marca o início da entidade com B
                    entity_started = True
                else:
                    tags[i] = f'I-{label}'  # Marca os tokens subsequentes com I
    
    return tags

# Função para quebrar o texto em tokens, manter os índices de start e end, e gerar as tags IOB
def tokenize_and_tag(text, entities):
    # Quebra o texto em tokens, considerando palavras e pontuações separadas
    tokens = list(re.finditer(r'\w+|[^\w\s]', text))  # Quebra palavras e pontuações
    tokens = [(token.group(0), token.start(), token.end()) for token in tokens if token.group(0).strip()]
    
    iob_tags = generate_iob_tags(tokens, entities)  # Gera as tags IOB
    
    token_data = []
    for i, (word, start, end) in enumerate(tokens):
        tag = iob_tags[i]
        token_data.append((word, tag, start, end))
    
    return token_data

# Função para processar o JSON e gerar o CSV
def process_json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Embaralhar documentos
    random.shuffle(data)
    
    csv_data = []
    sentence_id = 0
    item = 0
    
    for doc_index, document in enumerate(data):
        doc_id = doc_index + 1  # Identificador do documento como número sequencial
        text = document['text'].replace('#', '').replace('*', '')  # Remove marcações
        entities = document['entities']
        
        # Determina a partição do documento
        partition = random.randint(1, 10)
        training_test = 'training' if partition <= 7 else 'test' if partition <= 9 else 'validation'

        # Quebra o texto em sentenças
        sentences = re.split(r'(?<=\.)\s', text)  # Dividir as sentenças com base em pontuações seguidas de espaços
        total_sentences = len(sentences)
        
        # Tokenizar e gerar tags para cada sentença
        for sentence in sentences:
            token_data = tokenize_and_tag(sentence, entities)

            for word, tag, start, end in token_data:
                csv_data.append([item, word, tag, sentence_id, start, end, doc_id, partition, training_test])
                item += 1
            
            sentence_id += 1
    
    # Escrever os dados no CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['item', 'token', 'tag', 'sentence', 'start', 'end', 'document', 'partition', 'trainingTest'])
        writer.writerows(csv_data)
    
    print(f"Arquivo CSV gerado em {csv_file}")

def main():
    input_json = 'processed_patents.json'  # Arquivo JSON de entrada
    output_csv = 'patents_dataset.csv'      # Arquivo CSV de saída
    
    process_json_to_csv(input_json, output_csv)

if __name__ == "__main__":
    main()
