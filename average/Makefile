all: average

average: main.o
	gcc -no-pie -z noexecstack main.o -o average

main.o: main.asm
	nasm -f elf64 main.asm -o main.o

run: average
	./average data.txt

clean:
	rm -f average main.o
