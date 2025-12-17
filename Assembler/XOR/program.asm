global main
extern GetStdHandle
extern WriteConsoleA
extern ExitProcess

section .data
    message db "Computer", 0
    len equ $-message

section .bss
    result resb len
    bytesWritten resd 1

section .text
main:
    push rbx
    push rsi
    push rdi
    
    mov rcx, len
    dec rcx              
    jz .print_result     
    
    mov rsi, message     
    mov rdi, result      
    
    xor rdx, rdx        
.cycle:
    mov al, [rsi + rdx]
    mov bl, [rsi + rdx + 1]
    xor al, bl
    mov [rdi + rdx], al
    inc rdx
    cmp rdx, rcx
    jb .cycle
    
    mov al, [rsi + rcx]      
    mov bl, [rsi]            
    xor al, bl
    mov [rdi + rcx], al
    
    ; ===== ВЫВОД РЕЗУЛЬТАТА =====
.print_result:
    ; 1. Получаем хэндл консоли (STD_OUTPUT_HANDLE = -11)
    mov ecx, -11            ; nStdHandle
    call GetStdHandle       ; результат в RAX
    
    ; 2. Выводим строку
    mov rcx, rax            ; hConsoleOutput (первый аргумент)
    mov rdx, result         ; lpBuffer (второй аргумент)
    mov r8, len             ; nNumberOfBytesToWrite (третий)
    mov r9, bytesWritten    ; lpNumberOfBytesWritten (четвертый)
    
    ; Пятый аргумент (lpReserved) должен быть в стеке
    ; Выравниваем стек до 16 байт + shadow space (32 байта)
    sub rsp, 40             ; 32 (shadow space) + 8 (аргумент)
    mov qword [rsp + 32], 0 ; lpReserved = NULL
    call WriteConsoleA
    add rsp, 40             ; очищаем стек
    
    pop rdi
    pop rsi
    pop rbx
    
    mov ecx, 0              ; код выхода
    call ExitProcess