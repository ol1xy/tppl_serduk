section .data
    err_msg db ": файл испорчен", 10
    err_len equ $ - err_msg
    colon_space db ": "
    colon_len equ $ - colon_space
    newline db 10

section .bss
    filename_ptr resq 1
    fd resq 1
    bytes_read resq 1
    buffer resb 65536
    arr_x resq 4096
    arr_y resq 4096
    count_x resq 1
    count_y resq 1
    avg resq 1
    num_buf resb 32

section .text
global _start

_start:
    cmp qword [rsp], 2
    jl exit_err_no_name

    mov rax, [rsp + 16]
    mov [filename_ptr], rax

    mov rax, 2
    mov rdi, [filename_ptr]
    xor rsi, rsi
    xor rdx, rdx
    syscall

    cmp rax, 0
    jl error

    mov [fd], rax

    mov rax, 0
    mov rdi, [fd]
    mov rsi, buffer
    mov rdx, 65535
    syscall

    cmp rax, 0
    jle close_and_error

    mov [bytes_read], rax

    mov rax, 3
    mov rdi, [fd]
    syscall

    mov rbx, [bytes_read]
    mov byte [buffer + rbx], 0

    mov rsi, buffer
    mov rdi, arr_x
    call parse_line
    cmp rax, 0
    je error
    mov [count_x], rcx

    mov rdi, arr_y
    call parse_line
    cmp rax, 0
    je error
    mov [count_y], rcx

skip_trailing_whitespace:
    mov al, [rsi]
    cmp al, ' '
    je .skip
    cmp al, 9
    je .skip
    cmp al, 10
    je .skip
    cmp al, 13
    je .skip
    jmp .done
.skip:
    inc rsi
    jmp skip_trailing_whitespace
.done:
    cmp byte [rsi], 0
    jne error

    mov rax, [count_x]
    cmp rax, [count_y]
    jne error
    cmp rax, 0
    je error

    xor rbx, rbx
    xor r12, r12

calc_loop:
    cmp rbx, [count_x]
    jge calc_average
    mov rax, [arr_x + rbx*8]
    sub rax, [arr_y + rbx*8]
    add r12, rax
    inc rbx
    jmp calc_loop

calc_average:
    mov rax, r12
    cqo
    idiv qword [count_x]
    mov [avg], rax

    call print_filename

    mov rax, 1
    mov rdi, 1
    mov rsi, colon_space
    mov rdx, colon_len
    syscall

    mov rax, [avg]
    call print_number

    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall

close_and_error:
    mov rax, 3
    mov rdi, [fd]
    syscall
    jmp error

exit_err_no_name:
    mov rax, 60
    mov rdi, 1
    syscall

error:
    call print_filename
    mov rax, 1
    mov rdi, 1
    mov rsi, err_msg
    mov rdx, err_len
    syscall

    mov rax, 60
    mov rdi, 1
    syscall

parse_line:
    xor rcx, rcx

.next_token:
    call skip_spaces
    mov al, [rsi]
    cmp al, 10
    je .end_line
    cmp al, 13
    je .end_line
    cmp al, 0
    je .end_line

    xor r8, r8
    cmp al, '-'
    je .is_minus
    cmp al, '+'
    je .is_plus
    jmp .read_digits

.is_minus:
    mov r8, 1
    inc rsi
    jmp .read_digits

.is_plus:
    inc rsi

.read_digits:
    mov al, [rsi]
    cmp al, '0'
    jb .parse_fail
    cmp al, '9'
    ja .parse_fail

    xor rax, rax

.digit_loop:
    movzx rdx, byte [rsi]
    cmp rdx, '0'
    jb .digits_done
    cmp rdx, '9'
    ja .digits_done
    sub rdx, '0'
    imul rax, 10
    add rax, rdx
    inc rsi
    jmp .digit_loop

.digits_done:
    test r8, r8
    jz .store_number
    neg rax

.store_number:
    mov [rdi + rcx*8], rax
    inc rcx

    call skip_spaces
    mov al, [rsi]
    cmp al, ','
    jne .check_eol
    inc rsi
    call skip_spaces
    mov al, [rsi]
    cmp al, 10
    je .parse_fail
    cmp al, 13
    je .parse_fail
    cmp al, 0
    je .parse_fail
    jmp .next_token

.check_eol:
    cmp al, 10
    je .end_line
    cmp al, 13
    je .end_line
    cmp al, 0
    je .end_line
    jmp .parse_fail

.end_line:
    cmp al, 13
    jne .check_nl
    inc rsi
    cmp byte [rsi], 10
    jne .check_empty
    inc rsi
    jmp .check_empty

.check_nl:
    cmp al, 10
    jne .check_empty
    inc rsi

.check_empty:
    cmp rcx, 0
    je .parse_fail
    mov rax, 1
    ret

.parse_fail:
    xor rax, rax
    ret

skip_spaces:
    mov al, [rsi]
    cmp al, ' '
    je .do_skip
    cmp al, 9
    je .do_skip
    ret
.do_skip:
    inc rsi
    jmp skip_spaces

print_filename:
    mov rsi, [filename_ptr]
    xor rdx, rdx
.len_loop:
    cmp byte [rsi + rdx], 0
    je .print
    inc rdx
    jmp .len_loop
.print:
    mov rax, 1
    mov rdi, 1
    syscall
    ret

print_number:
    push rbx
    push r12

    mov r12, rax
    cmp r12, 0
    jge .check_zero

    mov byte [num_buf], '-'
    mov rax, 1
    mov rdi, 1
    mov rsi, num_buf
    mov rdx, 1
    syscall

    neg r12

.check_zero:
    cmp r12, 0
    jne .non_zero

    mov byte [num_buf], '0'
    mov rax, 1
    mov rdi, 1
    mov rsi, num_buf
    mov rdx, 1
    syscall
    pop r12
    pop rbx
    ret

.non_zero:
    mov rax, r12
    mov rbx, 10
    lea rdi, [num_buf + 31]
    mov byte [rdi], 0

.convert_loop:
    xor rdx, rdx
    div rbx
    add dl, '0'
    dec rdi
    mov [rdi], dl
    test rax, rax
    jnz .convert_loop

    lea rdx, [num_buf + 31]
    sub rdx, rdi
    mov rsi, rdi
    mov rax, 1
    mov rdi, 1
    syscall

    pop r12
    pop rbx
    ret
