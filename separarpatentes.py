import json
import re

# Função para ler e processar o arquivo JSON
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Função para eliminar patentes não anotadas e adicionar identificadores
def process_patents(data):
    processed_data = []
    annotations = data.get('annotations', [])

    for i, annotation in enumerate(annotations):
        text = annotation[0]
        entity_data = annotation[1].get('entities', [])

        # Verificar se há entidades anotadas
        if entity_data:
            # Adicionar identificador de final de sentença #
            sentences = re.split(r'([.!?])', text)
            processed_text = ''.join([s + '#' if s in '.!?' else s for s in sentences])

            # Adicionar identificador de final de patente *
            processed_text += '*'

            processed_data.append({
                'document_id': f'document_{i+1}',
                'text': processed_text,
                'entities': entity_data
            })

    return processed_data

def main():
    input_file = 'final_annotations.json'  # Nome do arquivo JSON de entrada
    output_file = 'processed_patents.json'  # Nome do arquivo JSON de saída

    data = read_json(input_file)
    processed_data = process_patents(data)

    if processed_data:
        # Salvar o resultado processado em um novo arquivo JSON
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)
        
        print(f"Patentes processadas salvas em {output_file}")
    else:
        print("Nenhuma patente processada.")

if __name__ == "__main__":
    main()
