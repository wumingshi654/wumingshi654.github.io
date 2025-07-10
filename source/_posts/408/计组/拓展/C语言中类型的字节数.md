---
title: C语言中类型的字节数
date: 2025-06-22 17:27:27
categories:
    - 408
    - 计算机组成原理
    - 拓展
---

C语言中用signed声明的一定为补码，unsigned则不是，如果没有明确声明则取决于特定的编译器或平台等。

| 数据类型 (Data Type) | 典型32位系统字节数 | 典型64位系统字节数 | 备注 |
| --- | --- | --- | --- |
| `char` | 1 | 1 | C标准规定 `sizeof(char)` 永远为1，是最小的内存单位 |
| `signed char` | 1 | 1 | |
| `unsigned char` | 1 | 1 | |
| `short` / `short int` | 2 | 2 | |
| `unsigned short` | 2 | 2 | |
| `int` | 4 | 4 | |
| `unsigned int` | 4 | 4 | |
| `long` / `long int` | 4 | **4 或 8** | 这是最常见的区别点。64位Windows下为4字节，64位Linux和macOS下为8字节 |
| `unsigned long` | 4 | **4 或 8** | 同上 |
| `long long` / `long long int` | 8 | 8 | C99标准引入，提供至少64位的整型 |
| `unsigned long long` | 8 | 8 | |
| `_Bool` | 1 | 1 | C99标准引入，通常占用1字节以方便寻址 |
| `float` | 4 | 4 | 单精度浮点数 |
| `double` | 8 | 8 | 双精度浮点数 |
| `long double` | 8, 12 或 16 | 10, 12 或 16 | 精度和大小最不确定的类型，强烈依赖于具体平台 |
| `(任意类型) *` | 4 | 8 | 指针的大小通常等于CPU的“字长”或地址总线的宽度 |
