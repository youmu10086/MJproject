<template>
    <el-table :data="tableData" :size="size" border :row-class-name="rowClassName" :default-sort="defaultSort"
        @selection-change="handleSelectionChange" :max-height="maxHeight" table-layout="fixed">
        <!-- 多选列 -->
        <el-table-column v-if="showSelection" type="selection"></el-table-column>

        <!-- 动态列 -->
        <el-table-column v-for="column in columns" :key="column.prop" :prop="column.prop" :label="column.label"
            :min-width="column.minWidth" :align="column.align || 'center'" :sortable="column.sortable || false"
            :show-overflow-tooltip="column.showOverflowTooltip || false">
            <template v-slot="scope">
                <slot :name="column.prop" :scope="scope">
                    {{ scope.row[column.prop] }}
                </slot>
            </template>
        </el-table-column>

        <!-- 操作列 -->
        <el-table-column v-if="$slots.actions" label="操作" :min-width="actionColumnWidth" align="center">
            <template v-slot="scope">
                <slot name="actions" :scope="scope"></slot>
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup lang="ts">
import { PropType } from 'vue';

const props = defineProps({
    tableData: {
        type: Array as PropType<any[]>,
        required: true,
    },
    columns: {
        type: Array as PropType<
            Array<{
                prop: string;
                label: string;
                minWidth?: string | number;
                align?: string;
                sortable?: boolean;
                showOverflowTooltip?: boolean;
            }>
        >,
        required: true,
    },
    size: {
        type: String as PropType<'' | 'small' | 'large' | 'default'>,
        default: 'small',
    },
    rowClassName: {
        type: Function as PropType<(row: any) => string>,
        default: () => '',
    },
    defaultSort: {
        type: Object as PropType<{ prop: string; order: 'ascending' | 'descending' }>,
        default: () => ({}),
    },
    maxHeight: {
        type: [String, Number],
        default: 400,
    },
    showSelection: {
        type: Boolean,
        default: false,
    },
    actionColumnWidth: {
        type: [String, Number],
        default: 240,
    },
});

const emit = defineEmits(['selection-change']);

const handleSelectionChange = (selection: any[]) => {
    emit('selection-change', selection);
};
</script>