global _start
 
section .text
number: dq 124   ; определяем объект number внутри секции .text
_start:
    mov rax, [rel number]   ; используем адрес number относительно регистра RIP
    ret   