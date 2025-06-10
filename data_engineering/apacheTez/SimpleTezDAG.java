public class SimpleTezDAG {
    public static void main(String[] args) throws Exception {
        TezConfiguration tezConf = new TezConfiguration();
        DAG dag = DAG.create("SimpleDAG");

        Vertex v1 = Vertex.create("v1", ProcessorDescriptor.create(TokenProcessor.class.getName()), 1);
        Vertex v2 = Vertex.create("v2", ProcessorDescriptor.create(LoggingProcessor.class.getName()), 1);

        dag.addVertex(v1).addVertex(v2);
        dag.addEdge(Edge.create(v1, v2, EdgeProperty.create(
                DataMovementType.ONE_TO_ONE,
                DataSourceType.PERSISTED,
                SchedulingType.SEQUENTIAL,
                OutputDescriptor.create(OrderedPartitionedKVOutput.class.getName()),
                InputDescriptor.create(OrderedGroupedInput.class.getName()))));

        TezClient tezClient = TezClient.create("SimpleTezApp", tezConf);
        tezClient.start();
        DAGClient dagClient = tezClient.submitDAG(dag);
        dagClient.waitForCompletion();
        tezClient.stop();
    }
}