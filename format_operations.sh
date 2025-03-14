#!/bin/bash

# Função para enviar mensagens de progresso
progress() {
    echo "PROGRESS:$1:$2"
}

# Verifica se recebeu os parâmetros necessários
if [ $# -lt 2 ]; then
    echo "Uso: $0 <dispositivo> <operação>"
    exit 1
fi

DEVICE="$1"
OPERATION="$2"

case "$OPERATION" in
    "format")
        # Desmonta todas as partições do dispositivo
        progress 10 "Desmontando partições..."
        for partition in "${DEVICE}"*; do
            umount "$partition" 2>/dev/null || true
        done
        
        # Cria uma nova tabela de partições
        progress 30 "Criando nova tabela de partições..."
        parted -s "$DEVICE" mklabel msdos
        
        # Cria uma partição primária usando todo o espaço
        progress 50 "Criando partição..."
        parted -s "$DEVICE" mkpart primary fat32 1MiB 100%
        
        # Aguarda o sistema reconhecer a nova partição
        progress 60 "Aguardando sistema..."
        sleep 2
        
        # Formata a partição como FAT32
        progress 80 "Formatando partição..."
        mkfs.fat -F32 "${DEVICE}1"
        
        progress 100 "Formatação concluída!"
        exit 0
        ;;
    *)
        echo "Operação desconhecida: $OPERATION"
        exit 1
        ;;
esac 