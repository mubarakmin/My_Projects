class_name State extends Node

## Stores a reference to the player that this state belongs to
static var player : Player


func _ready():
    pass

## What happens when the player enters this State?
func Enter() -> void:
    pass

## What happens when the player exits this State?
func Exit() -> void:
    pass

## What happens during the process update in this State?
func Process(_delta : float) -> State:
    return null

## What happens during the physics process update in this State?
func Physics (_delta : float) -> State:
    return null

## What happens when an input event is received in this State?
func HandleInput(_event : InputEvent) -> State:
    return null