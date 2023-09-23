<template>
    <el-radio-group v-model="size">
    <el-radio label="large">Large</el-radio>
    <el-radio>Default</el-radio>
    <el-radio label="small">Small</el-radio>
  </el-radio-group>

  <el-descriptions
    class="margin-top"
    title="违规用户信息收集"
    :column="3"
    :size="size"
    border
  >
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <user />
          </el-icon>
          车牌号
        </div>
      </template>
      SN793112
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <iphone />
          </el-icon>
          Telephone
        </div>
      </template>
      18100000000
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <location />
          </el-icon>
          Place
        </div>
      </template>
      Suzhou
    </el-descriptions-item>
  </el-descriptions>

</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'MyComponent',
  setup() {
    const size = ref('')
    const iconStyle = computed(() => {
      const marginMap = {
        large: '8px',
        default: '6px',
        small: '4px',
      }
      return {
        marginRight: marginMap[size.value] || marginMap.default,
      }
    })
    const blockMargin = computed(() => {
      const marginMap = {
        large: '32px',
        default: '28px',
        small: '24px',
      }
      return {
        marginTop: marginMap[size.value] || marginMap.default,
      }
    })
    return { size, iconStyle, blockMargin }
  },
}
</script>
