cmake_minimum_required(VERSION 3.10)

# set custom compiler
set(CMAKE_C_COMPILER ${CMAKE_CURRENT_LIST_DIR}/_cgt233/bin/cgpru.exe)


# set the project name
#project(Shepherd-Firmware C)
project(PRU0 C)
project(PRU1 C)
set(CMAKE_C_STANDARD 11)

# add the executable
add_executable(PRU0
        ${CMAKE_CURRENT_LIST_DIR}/pru0-shepherd-fw/main.c
        ${CMAKE_CURRENT_LIST_DIR}/pru0-shepherd-fw/ringbuffer.c
        ${CMAKE_CURRENT_LIST_DIR}/pru0-shepherd-fw/sampling.c
        ${CMAKE_CURRENT_LIST_DIR}/pru0-shepherd-fw/spi_transfer.asm
        ${CMAKE_CURRENT_LIST_DIR}/pru0-shepherd-fw/virtcap.c
        )

add_executable(PRU1
        ${CMAKE_CURRENT_LIST_DIR}/pru1-shepherd-fw/main.c
        )

target_compile_definitions(PRU0 PRIVATE PRU0)
target_compile_definitions(PRU1 PRIVATE PRU1)

# set includes
#target_include_directories(all PUBLIC
#        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/include
#        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/lib
#        ${CMAKE_CURRENT_LIST_DIR}/lib/include
#        ${CMAKE_CURRENT_LIST_DIR}/lib/src
#        ${CMAKE_CURRENT_LIST_DIR}/include
#        )

target_include_directories(PRU0 PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/pru0-shepherd-fw/include
        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/include/am335x
        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/include/
        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/lib/src/rpmsg_lib
        ${CMAKE_CURRENT_LIST_DIR}/lib/include
        ${CMAKE_CURRENT_LIST_DIR}/lib/src
        ${CMAKE_CURRENT_LIST_DIR}/include
        )

target_include_directories(PRU1 PRIVATE
#        ${CMAKE_CURRENT_LIST_DIR}/pru1-shepherd-fw
        ${CMAKE_CURRENT_LIST_DIR}/pru1-shepherd-fw/include
        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/include/am335x
        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/include/
        ${CMAKE_CURRENT_LIST_DIR}/_pssp57/lib/src/rpmsg_lib
        ${CMAKE_CURRENT_LIST_DIR}/lib/include
        ${CMAKE_CURRENT_LIST_DIR}/lib/src
        ${CMAKE_CURRENT_LIST_DIR}/include
        )

# TODO: pssp and lib should be interface libraries, with PRUs linking to it
