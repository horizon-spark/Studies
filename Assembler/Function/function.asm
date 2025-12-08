section .text

global _start

_start:

    mov ax, 0
    mov bx, 0
    mov cx, 0
    mov dx, 0

    call F

F:
    mov ax, 0b0000000011111111
    mov bx, 0b0000111100001111
    mov cx, 0b0011001100110011
    mov dx, 0b0101010101010101
    
    push ax
    OR ax, bx
    NOT cx
    OR ax, cx
    NOT cx
    NOT dx
    OR ax, dx
    NOT dx
    push ax
    mov ax, [rsp + 4]
    
    NOT bx
    OR ax, bx
    NOT bx
    OR ax, cx
    NOT dx
    OR ax, dx
    NOT dx
    push ax
    mov ax, [rsp + 8]
    
    NOT ax
    NOT bx
    OR ax, bx
    NOT bx
    OR ax, cx
    NOT dx
    OR ax, dx
    NOT dx
    push ax
    mov ax, [rsp + 12]	

    pop cx
    pop bx
    pop ax
    AND ax, bx
    AND ax, cx

    mov bx, 0
    mov cx, 0
    mov dx, 0
	