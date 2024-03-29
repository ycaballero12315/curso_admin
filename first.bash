#!/bin/bash
echo "Inserte el numero a sumar: "

read numero1

echo "Inserte el segundo numero: "

read numero2

resultado=$((numero1 + numero2))
echo "La suma de $numero1 + $numero2 = $resultado"
