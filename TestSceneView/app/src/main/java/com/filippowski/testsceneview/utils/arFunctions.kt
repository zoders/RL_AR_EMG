package com.filippowski.testsceneview.utils

import androidx.activity.ComponentActivity
import dev.romainguy.kotlin.math.Float3
import io.github.sceneview.ar.node.ArModelNode
import io.github.sceneview.ar.node.ArNode
import io.github.sceneview.ar.node.PlacementMode

fun createARModel(
    context: ComponentActivity,
    placementMode: PlacementMode,
    glbFileLocation: String,
    followHitPosition: Boolean,
    scale: Float
): ArModelNode {
    val modelNode = ArModelNode(
        placementMode = placementMode,
        followHitPosition = followHitPosition,
        instantAnchor = true,
    )
    modelNode.loadModelGlbAsync(
        context = context,
        glbFileLocation = glbFileLocation,
        autoAnimate = true,
        centerOrigin = null,
        scaleToUnits = scale,
        onError = { exception -> },
        onLoaded = { modelInstance -> }
    )
    return modelNode
}

fun move( node: ArNode, action: String, step: Float, axis: String = "x", orientation: Int = 1) {
    val sign = (action.toFloat() * 2 - 1) * orientation
    when(axis){
        "x" -> {
            val posX = node.position.x
            node.position.x = posX + (step * sign)
        }
        "z" -> {
            val posZ = node.position.z
            node.position.z = posZ + (step * sign)
        }
    }
}

fun reset(goal1: ArNode, goal2: ArNode, player: ArNode, pos: Map<String, Int>?, centerPos: Float3) {
    val step = getStep()
    if (pos != null) {
        goal1.position.x = pos["gX"]!! * (5 * step) + centerPos.x
        goal1.position.z = pos["gZ"]!! * (5 * step) + centerPos.z
        goal2.position.x = pos["aX"]!! * (5 * step) + centerPos.x
        goal2.position.z = 0f + centerPos.z
        player.position.x = 0f + centerPos.x
        player.position.z = 0f + centerPos.z
    }
}

fun getStep() = 0.25f
