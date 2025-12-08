section .text

global _start

_start:
	mov rax, 2
	call _func
_func:
	push rbx
	mov bx, ax
	shl ax, 2
	add ax, bx
	shl ax, 3
	add ax, bx
	shl ax, 1
	add ax, bx
	add ax, -49
	pop rbx
	ret