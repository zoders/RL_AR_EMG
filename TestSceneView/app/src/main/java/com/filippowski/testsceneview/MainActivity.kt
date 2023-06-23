package com.filippowski.testsceneview

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.filippowski.testsceneview.game.PlayerInfo
import com.filippowski.testsceneview.server.SocketServer
import com.filippowski.testsceneview.ui.theme.TestSceneViewTheme
import io.github.sceneview.ar.ARScene
import io.github.sceneview.ar.node.ArNode
import io.github.sceneview.ar.node.PlacementMode
import com.filippowski.testsceneview.utils.createARModel
import com.filippowski.testsceneview.utils.getStep
import com.filippowski.testsceneview.utils.move
import com.filippowski.testsceneview.utils.reset
import io.github.sceneview.ar.arcore.position

class MainActivity : ComponentActivity() {

    private var nodes = SnapshotStateList<ArNode>()
    private var playerInfo by mutableStateOf(PlayerInfo())
    private lateinit var server: SocketServer
    private val posCodes: Map<String, Map<String, Int>> = mapOf(
        "a" to mapOf("aX" to -1, "gX" to -1, "gZ" to 1),
        "b" to mapOf("aX" to 1, "gX" to 1, "gZ" to 1),
        "c" to mapOf("aX" to -1, "gX" to -1, "gZ" to -1),
        "d" to mapOf("aX" to 1, "gX" to 1, "gZ" to -1),
    )
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val context = this
        server = SocketServer(this)
        server.start()

        setContent {
            TestSceneViewTheme {
                nodes = remember { mutableStateListOf<ArNode>() }
                Column {
                    ARScreen(context, modifier = Modifier
                        .fillMaxWidth()
                        .weight(10f), nodes, playerInfo)
                    BottomBar(modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .align(Alignment.CenterHorizontally),
                        nodes = nodes,
                    )
                }
            }
        }
    }
    var toast: Toast? = null
    fun getMessage(message: String) {
        runOnUiThread {
            if (toast != null) {
                toast?.cancel()
            }
            if (message == "0" || message == "1") {
                if (!nodes.isEmpty()) {
                    if (playerInfo.reward < 5)
                        move(nodes[0], message, getStep())
                    else {
                        var orientation = -1
                        if (playerInfo.posCode in listOf("b", "d")) {
                            orientation = 1
                        }
                        move(nodes[0], message, getStep(), "z", orientation)
                    }
                    playerInfo.reward++
                }
            }
            if (message in posCodes.keys) {
                reset(nodes[2], nodes[1], nodes[0], posCodes[message], playerInfo.pos)
                playerInfo.posCode = message
                playerInfo.penalty = 0
                playerInfo.reward = 0
            }
            if (message == "p") {
                playerInfo.penalty--
            }

            Toast.makeText(
                this,
                "score: ${(playerInfo.reward
                        + playerInfo.penalty
                        )}",
                Toast.LENGTH_SHORT
            ).show()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        server.stopServer()
    }
}

@Composable
fun ARScreen(
    context: ComponentActivity,
    modifier: Modifier,
    nodes: SnapshotStateList<ArNode>,
    playerInfo: PlayerInfo
) {

    Box(modifier = modifier) {
        ARScene(
            modifier = Modifier.fillMaxSize(),
            nodes = nodes,
            planeRenderer = true,
            onCreate = { arSceneView ->

                arSceneView.children

                val modelDrone = createARModel(
                    context = context,
                    placementMode = PlacementMode.BEST_AVAILABLE,
                    glbFileLocation = "quadrocopter_drone_-_animated.glb",
                    scale = 0.5f,
                    followHitPosition = false
                )
                nodes.add(modelDrone)
                val goalNode = createARModel(
                    context = context,
                    placementMode = PlacementMode.BEST_AVAILABLE,
                    glbFileLocation = "magic_ring_-_green.glb",
                    scale = 0.5f,
                    followHitPosition = false
                )
                nodes.add(goalNode)
                val axisGoalNode = createARModel(
                    context = context,
                    placementMode = PlacementMode.BEST_AVAILABLE,
                    glbFileLocation = "magic_ring_-_red.glb",
                    scale = 0.5f,
                    followHitPosition = false
                )
                nodes.add(axisGoalNode)
            },
            onSessionCreate = { session ->
                // Configure the ARCore session
                Toast.makeText(context, nodes[0].position.x.toString(), Toast.LENGTH_SHORT)
            },
            onFrame = { arFrame ->
                // Retrieve ARCore frame update
            },
            onTap = { hitResult ->
                playerInfo.pos = hitResult.hitPose.position
                nodes[0].worldPosition = playerInfo.pos
                nodes[1].worldPosition = playerInfo.pos
                nodes[2].worldPosition = playerInfo.pos
            }
        )

    }
}


@Composable
fun BottomBar(modifier: Modifier, nodes: SnapshotStateList<ArNode>) {
    Row(modifier = modifier, ) {
        Button(
            onClick = {
                if (!nodes.isEmpty()) {
                    move(nodes[0], "0", getStep())
                }
            }
        ) {
            Text(
                text = "left"
            )
        }
        Button(
            onClick = {
                if (!nodes.isEmpty()) {
                    move(nodes[0], "1", getStep())
                }
            }
        ) {
            Text(
                text = "right"
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    TestSceneViewTheme {
        //Buttons(modifier = Modifier)
    }
}