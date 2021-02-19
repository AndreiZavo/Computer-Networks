#include <stdio.h>
#ifndef _WIN32

#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netinet/ip.h>
// for inet_ntoa
#include <arpa/inet.h>
// for close
#include <unistd.h> 
#define closesocket close
typedef int SOCKET;
#else
#define _WINSOCK_DEPRECATED_NO_WARNINGS
// on Windows include and link these things
#include<WinSock2.h>
// for uint16_t 
#include<cstdint>
// for inet_ntoa
#include<wsipv6ok.h>
// this is how we can link a library directly from the source code with the VC++ compiler �
// otherwise got o project settings and link to it explicitly
#pragma comment(lib,"Ws2_32.lib")

#endif

#include <string.h>


int main() {

    // initialize the Windows Sockets Library only when compiled on Windows
#ifdef WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) < 0) {
        printf("Error initializing the Windows Sockets Library");
        return -1;
    }
#endif

    int c;


    uint16_t length, length_be, b[10], suma;

    //  AF_INET - communication domain
    // SOCK_STREAM - communication type
    // 0 - protocol (IP)
    c = socket(AF_INET, SOCK_STREAM, 0);
    if (c < 0) {
        printf("Eroare la crearea socketului client\n");
        return 1;
    }


    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));

    server.sin_port = htons(1234);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");



    if (connect(c, (struct sockaddr*) & server, sizeof(server)) < 0) {
        printf("Eroare la conectarea la server\n");
        return 1;
    }


    printf("length = ");
#ifdef WIN32
    scanf_s("%hu", &length);
#else
    scanf("%hu", &length);
#endif
    for (int i = 0; i < length; i++) {
        printf("b[%d] = ", i);
#ifdef WIN32
        scanf_s("%hu", &b[i]);
#else
        scanf("%hu", &b[i]);
#endif
    }

    length_be = htons(length);
    send(c, (char*)&length_be, sizeof(length_be), 0);
    for (int i = 0; i < length; i++) {
        b[i] = htons(b[i]);
        send(c, (char*)&b[i], sizeof(b[i]), 0);
    }

    
   

    recv(c, (char*)&suma, sizeof(suma), 0);

    suma = ntohs(suma);

    printf("Suma este %hu\n", suma);

    getchar();
    getchar();

#ifdef WIN32
    // Release the Windows Sockets Library
    WSACleanup();
    closesocket(c);
#else
    close(c);
#endif
}

