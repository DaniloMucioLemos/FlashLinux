# FlashLinux

Utilitário especializado para formatação e preparação de dispositivos USB com suporte a sistemas de arquivos EXT4 e FAT32, otimizado para criação de mídias bootáveis com distribuições Linux.

## Recursos

- Formatação de dispositivos USB (EXT4/FAT32)
- Download de imagens ISO de distribuições Linux populares
- Gravação de imagens ISO em dispositivos USB
- Interface moderna e intuitiva
- Suporte a múltiplos idiomas (Português, Español, English)
- Temas claro e escuro

## Requisitos

- Sistema Linux
- Python 3.6 ou superior
- Privilégios de administrador

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/DaniloMucioLemos/FlashLinux.git
cd FlashLinux
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as permissões:
```bash
sudo cp com.flashlinux.pkexec.policy /usr/share/polkit-1/actions/
sudo chmod +x format_operations.sh auth_check.sh
```

4. Instale o atalho do desktop:
```bash
sudo cp flashlinux.desktop /usr/share/applications/
```

## Uso

Execute o programa através do menu de aplicativos ou via terminal:
```bash
python3 flashlinux.py
```

## Funcionalidades

1. **Formatação USB**
   - Selecione o dispositivo
   - Escolha o sistema de arquivos
   - Formate com segurança

2. **Download de Imagens**
   - Escolha entre distribuições populares
   - Download com controle de progresso
   - Verificação automática de links

3. **Gravação de ISO**
   - Selecione arquivo ISO local
   - Grave em dispositivo USB
   - Monitore o progresso

## Suporte

- Email: danmuciolemos@gmail.com
- GitHub Issues: [Reportar Problema](https://github.com/DaniloMucioLemos/FlashLinux/issues)

## Licença

Este projeto está licenciado sob a MIT License. 