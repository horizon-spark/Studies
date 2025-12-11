section .text

global _start

_func:    
    mov  rax, 0b0000000011111111
    mov  rbx, 0b0000111100001111
    mov  rcx, 0b0011001100110011
    mov rdx, 0b0101010101010101

    push  rax
    OR  rax,  rbx
    NOT  rcx
    OR  rax,  rcx
    NOT  rcx
    NOT rdx
    OR  rax, rdx
    NOT rdx
    push  rax
    mov  rax, [rsp + 8]
    
    NOT  rbx
    OR  rax,  rbx
    NOT  rbx
    OR  rax,  rcx
    NOT rdx
    OR  rax, rdx
    NOT rdx
    push  rax
    mov  rax, [rsp + 16]
    
    NOT  rax
    NOT  rbx
    OR  rax,  rbx
    NOT  rbx
    OR  rax,  rcx
    NOT rdx
    OR  rax, rdx
    NOT rdx
    push  rax
    mov  rax, [rsp + 24]	

    pop  rcx
    pop  rbx
    pop  rax
    pop  rdx
    AND  rax,  rbx
    AND  rax,  rcx
   
    ret

_start:
    call _func
    ret
	